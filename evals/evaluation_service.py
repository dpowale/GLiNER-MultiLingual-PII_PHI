"""
Evaluation Service for NER Dataset using GLiNER PII Model
Tests the model against the generated ner_evaluation_dataset.json
"""
import json
import logging
import warnings
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from gliner import GLiNER

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class EntityMatch:
    """Represents a match between predicted and ground truth entity"""
    predicted_text: str
    predicted_label: str
    predicted_start: int
    predicted_end: int
    predicted_score: float
    ground_truth_text: Optional[str] = None
    ground_truth_label: Optional[str] = None
    ground_truth_start: Optional[int] = None
    ground_truth_end: Optional[int] = None
    match_type: str = "none"  # exact, partial, label_mismatch, none

@dataclass
class EvaluationMetrics:
    """Metrics for a single evaluation"""
    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    true_negatives: int = 0  # Correctly identified no-PII sentences
    partial_matches: int = 0
    label_mismatches: int = 0
    
    @property
    def precision(self) -> float:
        if self.true_positives + self.false_positives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_positives)
    
    @property
    def recall(self) -> float:
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_negatives)
    
    @property
    def f1_score(self) -> float:
        if self.precision + self.recall == 0:
            return 0.0
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)
    
    @property
    def specificity(self) -> float:
        """True negative rate - how well we avoid false positives on negative samples"""
        if self.true_negatives + self.false_positives == 0:
            return 0.0
        return self.true_negatives / (self.true_negatives + self.false_positives)

@dataclass
class LanguageMetrics:
    """Metrics aggregated by language"""
    language: str
    total_samples: int = 0
    positive_samples: int = 0
    negative_samples: int = 0
    metrics: EvaluationMetrics = field(default_factory=EvaluationMetrics)
    entity_type_metrics: Dict[str, EvaluationMetrics] = field(default_factory=dict)

@dataclass
class EvaluationReport:
    """Complete evaluation report"""
    total_samples: int = 0
    overall_metrics: EvaluationMetrics = field(default_factory=EvaluationMetrics)
    language_metrics: Dict[str, LanguageMetrics] = field(default_factory=dict)
    entity_type_metrics: Dict[str, EvaluationMetrics] = field(default_factory=dict)
    failed_samples: List[Dict[str, Any]] = field(default_factory=list)

class NERDatasetEvaluator:
    """Evaluates GLiNER model against the NER evaluation dataset"""
    
    # Map dataset labels to model-compatible labels (using underscore format)
    LABEL_MAPPING = {
        "person": "person",
        "organization": "organization",
        "phone number": "phone_number",
        "phone_number": "phone_number",
        "mobile phone number": "mobile_phone_number",
        "mobile_phone_number": "mobile_phone_number",
        "fax number": "fax_number",
        "fax_number": "fax_number",
        "address": "address",
        "passport number": "passport_number",
        "passport_number": "passport_number",
        "email": "email_address",  # Model outputs 'email', ground truth uses 'email_address'
        "email address": "email_address",
        "email_address": "email_address",
        "credit card number": "credit_card_number",
        "credit_card_number": "credit_card_number",
        "credit card brand": "credit_card_brand",
        "credit_card_brand": "credit_card_brand",
        "credit card expiration date": "credit_card_expiration_date",
        "credit_card_expiration_date": "credit_card_expiration_date",
        "credit card cvv": "credit_card_cvv",
        "credit_card_cvv": "credit_card_cvv",
        "social security number": "social_security_number",
        "social_security_number": "social_security_number",
        "date of birth": "date_of_birth",
        "date_of_birth": "date_of_birth",
        "bank account number": "bank_account_number",
        "bank_account_number": "bank_account_number",
        "medication": "medication",
        "medical condition": "medical_condition",
        "medical_condition": "medical_condition",
        "driver's license number": "driver_license_number",
        "driver_license_number": "driver_license_number",
        "tax identification number": "tax_identification_number",
        "tax_identification_number": "tax_identification_number",
        "identity card number": "identity_card_number",
        "identity_card_number": "identity_card_number",
        "national id number": "national_id_number",
        "national_id_number": "national_id_number",
        "ip address": "ip_address",
        "ip_address": "ip_address",
        "iban": "iban",
        "license plate number": "license_plate_number",
        "license_plate_number": "license_plate_number",
        "vehicle registration number": "vehicle_registration_number",
        "vehicle_registration_number": "vehicle_registration_number",
        "passport expiration date": "passport_expiration_date",
        "passport_expiration_date": "passport_expiration_date",
        "flight number": "flight_number",
        "flight_number": "flight_number",
        "social media handle": "social_media_handle",
        "social_media_handle": "social_media_handle",
        "username": "username",
        "digital signature": "digital_signature",
        "digital_signature": "digital_signature",
        "student id number": "student_id_number",
        "student_id_number": "student_id_number",
        "transaction number": "transaction_number",
        "transaction_number": "transaction_number",
        "landline phone number": "landline_phone_number",
        "landline_phone_number": "landline_phone_number",
    }
    
    def __init__(self, model_name: str = "urchade/gliner_multi_pii-v1", threshold: float = 0.4):
        """Initialize the evaluator with the GLiNER model"""
        self.threshold = threshold
        logger.info(f"Loading GLiNER model: {model_name}")
        self.model = GLiNER.from_pretrained(model_name)
        logger.info("Model loaded successfully")
        
        # Define labels to extract - consistent with main_service.py
        self.extraction_labels = [
            "person",
            "organization", 
            "phone_number",
            "address",
            "passport_number",
            "email",
            "email_address",
            "credit_card_number",
            "credit_card_brand",
            "credit_card_expiration_date",
            "credit_card_cvv",
            "social_security_number",
            "date_of_birth",
            "mobile_phone_number",
            "fax_number",
            "bank_account_number",
            "iban",
            "medication",
            "medical_condition",
            "tax_identification_number",
            "national_id_number",
            "ip_address",
            "username",
            "digital_signature",
            "license_plate_number",
            "vehicle_registration_number",
            "passport_expiration_date",
            "flight_number",
            "transaction_number",
            "social_media_handle",
            "student_id_number",
            "landline_phone_number"
        ]
    
    def load_dataset(self, dataset_path: str = "ner_evaluation_dataset.json") -> List[Dict[str, Any]]:
        """Load the NER evaluation dataset"""
        logger.info(f"Loading dataset from: {dataset_path}")
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        logger.info(f"Loaded {len(dataset)} samples")
        return dataset
    
    def normalize_label(self, label: str) -> str:
        """Normalize label for comparison"""
        label_lower = label.lower().strip()
        return self.LABEL_MAPPING.get(label_lower, label_lower)
    
    def compute_overlap(self, start1: int, end1: int, start2: int, end2: int) -> float:
        """Compute overlap ratio between two spans"""
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        
        if overlap_start >= overlap_end:
            return 0.0
        
        overlap_length = overlap_end - overlap_start
        span1_length = end1 - start1
        span2_length = end2 - start2
        
        # Return IoU (Intersection over Union)
        union_length = span1_length + span2_length - overlap_length
        return overlap_length / union_length if union_length > 0 else 0.0
    
    def match_entities(
        self, 
        predicted: List[Dict[str, Any]], 
        ground_truth: List[Dict[str, Any]],
        overlap_threshold: float = 0.5
    ) -> Tuple[List[EntityMatch], EvaluationMetrics]:
        """Match predicted entities to ground truth entities"""
        metrics = EvaluationMetrics()
        matches = []
        
        gt_matched = set()
        pred_matched = set()
        
        # First pass: find exact and partial matches
        for p_idx, pred in enumerate(predicted):
            pred_label = self.normalize_label(pred.get("label", ""))
            pred_start = pred.get("start", 0)
            pred_end = pred.get("end", 0)
            
            best_match = None
            best_overlap = 0.0
            best_gt_idx = -1
            
            for g_idx, gt in enumerate(ground_truth):
                if g_idx in gt_matched:
                    continue
                
                gt_label = self.normalize_label(gt.get("label", ""))
                gt_start = gt.get("start", 0)
                gt_end = gt.get("end", 0)
                
                overlap = self.compute_overlap(pred_start, pred_end, gt_start, gt_end)
                
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_match = gt
                    best_gt_idx = g_idx
            
            match = EntityMatch(
                predicted_text=pred.get("text", ""),
                predicted_label=pred_label,
                predicted_start=pred_start,
                predicted_end=pred_end,
                predicted_score=pred.get("score", 0.0)
            )
            
            if best_match and best_overlap >= overlap_threshold:
                gt_label = self.normalize_label(best_match.get("label", ""))
                match.ground_truth_text = best_match.get("text", "")
                match.ground_truth_label = gt_label
                match.ground_truth_start = best_match.get("start", 0)
                match.ground_truth_end = best_match.get("end", 0)
                
                if best_overlap >= 0.9 and pred_label == gt_label:
                    match.match_type = "exact"
                    metrics.true_positives += 1
                elif pred_label == gt_label:
                    match.match_type = "partial"
                    metrics.partial_matches += 1
                    metrics.true_positives += 1  # Count partial as TP for recall
                else:
                    match.match_type = "label_mismatch"
                    metrics.label_mismatches += 1
                    metrics.false_positives += 1
                
                gt_matched.add(best_gt_idx)
                pred_matched.add(p_idx)
            else:
                match.match_type = "none"
                metrics.false_positives += 1
            
            matches.append(match)
        
        # Count unmatched ground truth as false negatives
        for g_idx, gt in enumerate(ground_truth):
            if g_idx not in gt_matched:
                metrics.false_negatives += 1
        
        return matches, metrics
    
    def evaluate_sample(self, sample: Dict[str, Any]) -> Tuple[List[EntityMatch], EvaluationMetrics]:
        """Evaluate a single sample"""
        text = sample.get("text", "")
        ground_truth = sample.get("entities", [])
        
        # Get predictions from model
        try:
            predictions = self.model.predict_entities(
                text,
                self.extraction_labels,
                threshold=self.threshold,
                flat_ner=True
            )
        except Exception as e:
            logger.error(f"Error predicting entities: {e}")
            predictions = []
        
        return self.match_entities(predictions, ground_truth)
    
    def evaluate_dataset(
        self, 
        dataset_path: str = "ner_evaluation_dataset.json",
        verbose: bool = True
    ) -> EvaluationReport:
        """Evaluate the entire dataset and generate a report"""
        dataset = self.load_dataset(dataset_path)
        report = EvaluationReport(total_samples=len(dataset))
        
        for idx, sample in enumerate(dataset):
            language = sample.get("language", "Unknown")
            
            # Initialize language metrics if needed
            if language not in report.language_metrics:
                report.language_metrics[language] = LanguageMetrics(language=language)
            
            lang_metrics = report.language_metrics[language]
            lang_metrics.total_samples += 1
            
            # Track if this is a positive or negative sample
            ground_truth = sample.get("entities", [])
            is_negative_sample = len(ground_truth) == 0
            
            if is_negative_sample:
                lang_metrics.negative_samples += 1
            else:
                lang_metrics.positive_samples += 1
            
            # Evaluate sample
            matches, metrics = self.evaluate_sample(sample)
            
            # For negative samples, track true negatives (no predictions on no-PII sentences)
            if is_negative_sample and metrics.false_positives == 0:
                metrics.true_negatives += 1
            
            # Aggregate overall metrics
            report.overall_metrics.true_positives += metrics.true_positives
            report.overall_metrics.false_positives += metrics.false_positives
            report.overall_metrics.false_negatives += metrics.false_negatives
            report.overall_metrics.true_negatives += metrics.true_negatives
            report.overall_metrics.partial_matches += metrics.partial_matches
            report.overall_metrics.label_mismatches += metrics.label_mismatches
            
            # Aggregate language metrics
            lang_metrics.metrics.true_positives += metrics.true_positives
            lang_metrics.metrics.false_positives += metrics.false_positives
            lang_metrics.metrics.false_negatives += metrics.false_negatives
            lang_metrics.metrics.true_negatives += metrics.true_negatives
            lang_metrics.metrics.partial_matches += metrics.partial_matches
            lang_metrics.metrics.label_mismatches += metrics.label_mismatches
            
            # Track entity type metrics
            for match in matches:
                label = match.ground_truth_label or match.predicted_label
                if label not in report.entity_type_metrics:
                    report.entity_type_metrics[label] = EvaluationMetrics()
                
                entity_metrics = report.entity_type_metrics[label]
                if match.match_type in ["exact", "partial"]:
                    entity_metrics.true_positives += 1
                elif match.match_type == "none":
                    entity_metrics.false_positives += 1
            
            # Track failed samples
            if metrics.false_negatives > 0 or metrics.false_positives > 0:
                report.failed_samples.append({
                    "index": idx,
                    "language": language,
                    "text": sample.get("text", "")[:100] + "...",
                    "false_positives": metrics.false_positives,
                    "false_negatives": metrics.false_negatives
                })
            
            if verbose and (idx + 1) % 20 == 0:
                logger.info(f"Processed {idx + 1}/{len(dataset)} samples")
        
        return report
    
    def print_report(self, report: EvaluationReport):
        """Print a formatted evaluation report"""
        print("\n" + "="*80)
        print("NER EVALUATION REPORT")
        print("="*80)
        
        # Calculate positive and negative sample counts
        total_positive = sum(lm.positive_samples for lm in report.language_metrics.values())
        total_negative = sum(lm.negative_samples for lm in report.language_metrics.values())
        
        print(f"\nTotal Samples Evaluated: {report.total_samples}")
        print(f"  - Positive Samples (with PII): {total_positive}")
        print(f"  - Negative Samples (no PII):   {total_negative}")
        
        print("\n" + "-"*40)
        print("OVERALL METRICS")
        print("-"*40)
        print(f"True Positives:   {report.overall_metrics.true_positives}")
        print(f"False Positives:  {report.overall_metrics.false_positives}")
        print(f"False Negatives:  {report.overall_metrics.false_negatives}")
        print(f"True Negatives:   {report.overall_metrics.true_negatives} / {total_negative} negative samples")
        print(f"Partial Matches:  {report.overall_metrics.partial_matches}")
        print(f"Label Mismatches: {report.overall_metrics.label_mismatches}")
        print(f"\nPrecision:   {report.overall_metrics.precision:.4f}")
        print(f"Recall:      {report.overall_metrics.recall:.4f}")
        print(f"F1 Score:    {report.overall_metrics.f1_score:.4f}")
        if total_negative > 0:
            print(f"Specificity: {report.overall_metrics.specificity:.4f} (true negative rate)")
        
        print("\n" + "-"*40)
        print("METRICS BY LANGUAGE")
        print("-"*40)
        print(f"{'Language':<12} {'Total':<8} {'Pos':<6} {'Neg':<6} {'Precision':<11} {'Recall':<11} {'F1':<11} {'TN':<6}")
        print("-"*80)
        for lang, lang_metrics in sorted(report.language_metrics.items()):
            tn_str = f"{lang_metrics.metrics.true_negatives}/{lang_metrics.negative_samples}" if lang_metrics.negative_samples > 0 else "N/A"
            print(f"{lang:<12} {lang_metrics.total_samples:<8} "
                  f"{lang_metrics.positive_samples:<6} "
                  f"{lang_metrics.negative_samples:<6} "
                  f"{lang_metrics.metrics.precision:<11.4f} "
                  f"{lang_metrics.metrics.recall:<11.4f} "
                  f"{lang_metrics.metrics.f1_score:<11.4f} "
                  f"{tn_str:<6}")
        
        print("\n" + "-"*40)
        print("METRICS BY ENTITY TYPE (Top 15)")
        print("-"*40)
        print(f"{'Entity Type':<30} {'TP':<8} {'Precision':<12} {'Recall':<12}")
        print("-"*60)
        sorted_entities = sorted(
            report.entity_type_metrics.items(),
            key=lambda x: x[1].true_positives,
            reverse=True
        )[:15]
        for entity_type, metrics in sorted_entities:
            print(f"{entity_type:<30} {metrics.true_positives:<8} "
                  f"{metrics.precision:<12.4f} "
                  f"{metrics.recall:<12.4f}")
        
        print("\n" + "="*80)
    
    def export_report(self, report: EvaluationReport, output_path: str = "evaluation_report.json"):
        """Export the evaluation report to JSON"""
        report_dict = {
            "total_samples": report.total_samples,
            "overall_metrics": {
                "true_positives": report.overall_metrics.true_positives,
                "false_positives": report.overall_metrics.false_positives,
                "false_negatives": report.overall_metrics.false_negatives,
                "partial_matches": report.overall_metrics.partial_matches,
                "label_mismatches": report.overall_metrics.label_mismatches,
                "precision": report.overall_metrics.precision,
                "recall": report.overall_metrics.recall,
                "f1_score": report.overall_metrics.f1_score
            },
            "language_metrics": {
                lang: {
                    "total_samples": lm.total_samples,
                    "precision": lm.metrics.precision,
                    "recall": lm.metrics.recall,
                    "f1_score": lm.metrics.f1_score,
                    "true_positives": lm.metrics.true_positives,
                    "false_positives": lm.metrics.false_positives,
                    "false_negatives": lm.metrics.false_negatives
                }
                for lang, lm in report.language_metrics.items()
            },
            "entity_type_metrics": {
                entity_type: {
                    "true_positives": metrics.true_positives,
                    "false_positives": metrics.false_positives,
                    "false_negatives": metrics.false_negatives,
                    "precision": metrics.precision,
                    "recall": metrics.recall,
                    "f1_score": metrics.f1_score
                }
                for entity_type, metrics in report.entity_type_metrics.items()
            },
            "sample_failures": report.failed_samples[:50]  # Limit to first 50
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report exported to: {output_path}")


def main():
    """Main entry point for evaluation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate GLiNER model on NER dataset")
    parser.add_argument(
        "--dataset", 
        type=str, 
        default="ner_evaluation_dataset.json",
        help="Path to the evaluation dataset"
    )
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.4,
        help="Confidence threshold for entity extraction"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="evaluation_report.json",
        help="Output path for the evaluation report"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Run evaluation
    evaluator = NERDatasetEvaluator(threshold=args.threshold)
    report = evaluator.evaluate_dataset(args.dataset, verbose=args.verbose)
    
    # Print and export report
    evaluator.print_report(report)
    evaluator.export_report(report, args.output)
    
    print(f"\nEvaluation complete! Report saved to: {args.output}")


if __name__ == "__main__":
    main()
