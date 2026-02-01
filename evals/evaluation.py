"""
PII/PHI Evaluation Script
Tests all evaluation datasets with GLiNER multilingual model
"""

import json
import os
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

def evaluate_dataset(model, data, dataset_name):
    """Evaluate a dataset and return metrics."""
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    
    for item in data:
        gold = {(e['text'].lower(), e['label']) for e in item['entities']}
        preds = model.predict_entities(item['text'], LABELS, threshold=0.3)
        pred = {(p['text'].lower(), p['label']) for p in preds}
        
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

def main():
    print('=' * 75)
    print('GLiNER Multilingual PII/PHI Evaluation')
    print('Model: urchade/gliner_multi_pii-v1')
    print('=' * 75)
    
    print('\nLoading model...')
    model = GLiNER.from_pretrained('urchade/gliner_multi_pii-v1')
    
    # Define datasets to evaluate
    datasets = [
        ('ner_evaluation_dataset.json', 'NER Evaluation (Original)', 'json'),
        ('medical_phi_dataset.json', 'Medical PHI', 'json'),
        ('travel_pii_dataset.json', 'Travel PII', 'json'),
        ('mixed_language_dataset.json', 'Mixed Language', 'json'),
        ('structured_pii_phi.csv', 'Structured CSV', 'csv'),
    ]
    
    all_results = []
    
    for filepath, name, filetype in datasets:
        if not os.path.exists(filepath):
            print(f'\nSkipping {name}: {filepath} not found')
            continue
        
        print(f'\nEvaluating {name}...')
        
        if filetype == 'json':
            data = load_json_dataset(filepath)
        else:
            data = load_csv_dataset(filepath)
        
        results = evaluate_dataset(model, data, name)
        all_results.append(results)
        print_results(results)
    
    # Print summary
    if all_results:
        print_summary(all_results)
    
    print('\nEvaluation complete.')

if __name__ == '__main__':
    main()
