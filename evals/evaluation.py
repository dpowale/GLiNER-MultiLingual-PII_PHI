"""
Comprehensive PII/PHI Evaluation Script
Tests all evaluation datasets with GLiNER multilingual model
"""

import json
import os
import csv
from datetime import datetime
from gliner import GLiNER
from collections import defaultdict

# All supported entity labels
LABELS = [
    'person', 'organization', 'address', 'passport_number', 'driver_license_number',
    'identity_card_number', 'flight_number', 'phone_number', 'mobile_phone_number',
    'email', 'credit_card_number', 'date_of_birth', 'passport_expiration_date',
    'vehicle_registration_number', 'insurance_number', 'bank_account_number',
    'social_security_number', 'transaction_number', 'national_id_number', 'cpf',
    'tax_identification_number', 'health_insurance_id_number', 'iban',
    'medical_condition', 'medication', 'credit_card_cvv', 'fax_number',
    'license_plate_number', 'student_id_number', 'date', 'location'
]

def load_json_dataset(filepath):
    """Load a JSON evaluation dataset."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_csv_dataset(filepath):
    """Load CSV dataset and convert to evaluation format."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) >= 8:
                entities = [
                    {'text': parts[0], 'label': 'person'},
                    {'text': parts[1], 'label': 'address'},
                    {'text': parts[2], 'label': 'phone_number'},
                    {'text': parts[3], 'label': 'email'},
                    {'text': parts[4], 'label': 'national_id_number'},
                    {'text': parts[5], 'label': 'date_of_birth'},
                    {'text': parts[6], 'label': 'medical_condition'},
                    {'text': parts[7], 'label': 'medication'},
                ]
                data.append({'text': line, 'entities': entities})
    return data

def evaluate_dataset(model, data, dataset_name, predictions_list=None):
    """Evaluate a dataset and return metrics. Optionally collect predictions."""
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    
    for item in data:
        gold = {(e['text'].lower(), e['label']) for e in item['entities']}
        preds = model.predict_entities(item['text'], LABELS, threshold=0.3)
        pred = {(p['text'].lower(), p['label']) for p in preds}
        
        # Collect predictions for CSV output if list provided
        if predictions_list is not None:
            gold_entities = [{'text': e['text'], 'label': e['label']} for e in item['entities']]
            pred_entities = [{'text': p['text'], 'label': p['label'], 'score': p.get('score', 0)} for p in preds]
            
            # Determine match status for each prediction
            matched_gold = set()
            pred_with_status = []
            for p in preds:
                p_key = (p['text'].lower(), p['label'])
                if p_key in gold:
                    status = 'TP'  # True Positive
                    matched_gold.add(p_key)
                else:
                    status = 'FP'  # False Positive
                pred_with_status.append({
                    'text': p['text'],
                    'label': p['label'],
                    'score': p.get('score', 0),
                    'status': status
                })
            
            # Find missed entities (False Negatives)
            missed = []
            for e in item['entities']:
                e_key = (e['text'].lower(), e['label'])
                if e_key not in matched_gold:
                    missed.append({'text': e['text'], 'label': e['label'], 'status': 'FN'})
            
            predictions_list.append({
                'dataset': dataset_name,
                'text': item['text'][:200] + '...' if len(item['text']) > 200 else item['text'],
                'full_text': item['text'],
                'ground_truth': gold_entities,
                'predictions': pred_with_status,
                'missed': missed,
                'language': item.get('language', 'unknown')
            })
        
        for label in LABELS:
            g = {t for t, l in gold if l == label}
            p = {t for t, l in pred if l == label}
            tp[label] += len(g & p)
            fp[label] += len(p - g)
            fn[label] += len(g - p)
    
    # Calculate metrics
    results = {'name': dataset_name, 'examples': len(data), 'labels': {}}
    t_tp, t_fp, t_fn = 0, 0, 0
    
    for label in LABELS:
        if tp[label] + fp[label] + fn[label] == 0:
            continue
        t_tp += tp[label]
        t_fp += fp[label]
        t_fn += fn[label]
        
        p = tp[label] / (tp[label] + fp[label]) if tp[label] + fp[label] > 0 else 0
        r = tp[label] / (tp[label] + fn[label]) if tp[label] + fn[label] > 0 else 0
        f = 2 * p * r / (p + r) if p + r > 0 else 0
        
        results['labels'][label] = {
            'tp': tp[label], 'fp': fp[label], 'fn': fn[label],
            'precision': p, 'recall': r, 'f1': f
        }
    
    # Overall metrics
    p = t_tp / (t_tp + t_fp) if t_tp + t_fp > 0 else 0
    r = t_tp / (t_tp + t_fn) if t_tp + t_fn > 0 else 0
    f = 2 * p * r / (p + r) if p + r > 0 else 0
    
    results['overall'] = {
        'tp': t_tp, 'fp': t_fp, 'fn': t_fn,
        'precision': p, 'recall': r, 'f1': f
    }
    
    return results

def print_results(results):
    """Print evaluation results for a dataset."""
    print()
    print('=' * 75)
    print(f"DATASET: {results['name']} ({results['examples']} examples)")
    print('=' * 75)
    
    header = f"{'Label':<30} {'TP':<5} {'FP':<5} {'FN':<5} {'Prec':<8} {'Rec':<8} {'F1':<8}"
    print(header)
    print('-' * 75)
    
    # Sort by support (tp + fn)
    sorted_labels = sorted(
        results['labels'].items(),
        key=lambda x: -(x[1]['tp'] + x[1]['fn'])
    )
    
    for label, m in sorted_labels:
        row = f"{label:<30} {m['tp']:<5} {m['fp']:<5} {m['fn']:<5} {m['precision']:<8.3f} {m['recall']:<8.3f} {m['f1']:<8.3f}"
        print(row)
    
    print('-' * 75)
    o = results['overall']
    overall = f"{'OVERALL':<30} {o['tp']:<5} {o['fp']:<5} {o['fn']:<5} {o['precision']:<8.3f} {o['recall']:<8.3f} {o['f1']:<8.3f}"
    print(overall)

def print_summary(all_results):
    """Print summary comparison of all datasets."""
    print()
    print('=' * 75)
    print('EVALUATION SUMMARY - ALL DATASETS')
    print('=' * 75)
    
    header = f"{'Dataset':<35} {'Examples':<10} {'Precision':<10} {'Recall':<10} {'F1':<10}"
    print(header)
    print('-' * 75)
    
    # Sort by F1 score descending
    sorted_results = sorted(all_results, key=lambda x: -x['overall']['f1'])
    
    for r in sorted_results:
        o = r['overall']
        row = f"{r['name']:<35} {r['examples']:<10} {o['precision']:<10.3f} {o['recall']:<10.3f} {o['f1']:<10.3f}"
        print(row)
    
    print('-' * 75)
    
    # Calculate average
    avg_p = sum(r['overall']['precision'] for r in all_results) / len(all_results)
    avg_r = sum(r['overall']['recall'] for r in all_results) / len(all_results)
    avg_f = sum(r['overall']['f1'] for r in all_results) / len(all_results)
    total_examples = sum(r['examples'] for r in all_results)
    
    avg_row = f"{'AVERAGE':<35} {total_examples:<10} {avg_p:<10.3f} {avg_r:<10.3f} {avg_f:<10.3f}"
    print(avg_row)
    
def save_detailed_predictions_json(predictions_list, output_path):
    """Save  predictions to JSON for analysis."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(predictions_list, f, ensure_ascii=False, indent=2)
    print(f"Detailed predictions (JSON) saved to: {output_path}")
    
def save_predictions_to_csv(predictions_list, output_path):
    """Save predictions to a CSV for analysis."""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'Dataset', 'Language', 'Text (truncated)', 
            'Ground Truth Entities', 'Predicted Entities', 
            'True Positives', 'False Positives', 'False Negatives (Missed)',
            'TP Count', 'FP Count', 'FN Count'
        ])
        
        for item in predictions_list:
            # Format ground truth
            gt_str = '; '.join([f"{e['label']}:{e['text']}" for e in item['ground_truth']])
            
            # Format predictions with scores
            pred_str = '; '.join([f"{p['label']}:{p['text']}({p['score']:.2f})" for p in item['predictions']])
            
            # Separate by status
            tp_list = [p for p in item['predictions'] if p['status'] == 'TP']
            fp_list = [p for p in item['predictions'] if p['status'] == 'FP']
            fn_list = item['missed']
            
            tp_str = '; '.join([f"{p['label']}:{p['text']}" for p in tp_list]) or '-'
            fp_str = '; '.join([f"{p['label']}:{p['text']}" for p in fp_list]) or '-'
            fn_str = '; '.join([f"{e['label']}:{e['text']}" for e in fn_list]) or '-'
            
            writer.writerow([
                item['dataset'],
                item['language'],
                item['text'],
                gt_str or '-',
                pred_str or '-',
                tp_str,
                fp_str,
                fn_str,
                len(tp_list),
                len(fp_list),
                len(fn_list)
            ])
    
    print(f"\nPredictions saved to: {output_path}")

def main():
    print('=' * 75)
    print('GLiNER Multilingual PII/PHI Evaluation')
    print('Model: urchade/gliner_multi_pii-v1')
    print('=' * 75)
    
    print('\nLoading model...')
    model = GLiNER.from_pretrained('urchade/gliner_multi_pii-v1')
    
    # Create predicted_output folder under data
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'predicted_output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Define datasets to evaluate
    datasets = [
        ('ner_evaluation_dataset.json', 'NER Evaluation (Original)', 'json'),
        ('medical_phi_dataset.json', 'Medical PHI', 'json'),
        ('travel_pii_dataset.json', 'Travel PII', 'json'),
        ('mixed_language_dataset.json', 'Mixed Language', 'json'),
        ('structured_pii_phi.csv', 'Structured CSV', 'csv'),
    ]
    
    all_results = []
    all_predictions = []
    
    for filepath, name, filetype in datasets:
        if not os.path.exists(filepath):
            print(f'\nSkipping {name}: {filepath} not found')
            continue
        
        print(f'\nEvaluating {name}...')
        
        # Separate predictions list for each dataset
        dataset_predictions = []
        
        if filetype == 'json':
            data = load_json_dataset(filepath)
        else:
            data = load_csv_dataset(filepath)
        
        results = evaluate_dataset(model, data, name, dataset_predictions)
        all_results.append(results)
        all_predictions.extend(dataset_predictions)
        print_results(results)
        
        # Save individual prediction file for this dataset to predicted_output folder
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_csv = os.path.join(output_dir, f'predictions_{base_name}.csv')
        output_json = os.path.join(output_dir, f'predictions_{base_name}.json')
        save_predictions_to_csv(dataset_predictions, output_csv)
        save_detailed_predictions_json(dataset_predictions, output_json)
    
    # Print summary
    if all_results:
        print_summary(all_results)
    
    print('\nEvaluation complete.')

if __name__ == '__main__':
    main()
