"""
Tests for PII/PHI entity extraction using GLiNER model
"""
import pytest
from gliner import GLiNER

# Load model once for all tests
@pytest.fixture(scope="module")
def model():
    """Load the GLiNER PII model"""
    return GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")


class TestPersonExtraction:
    """Test person name extraction"""
    
    def test_extract_single_person(self, model):
        text = "John Smith is a software engineer."
        entities = model.predict_entities(text, ["person"], threshold=0.5)
        
        assert len(entities) >= 1
        person_names = [e["text"] for e in entities if e["label"] == "person"]
        assert "John Smith" in person_names
    
    def test_extract_multiple_persons(self, model):
        text = "Jane Doe met with Bob Johnson at the conference."
        entities = model.predict_entities(text, ["person"], threshold=0.5)
        
        person_names = [e["text"] for e in entities if e["label"] == "person"]
        assert len(person_names) >= 2


class TestEmailExtraction:
    """Test email address extraction"""
    
    def test_extract_email(self, model):
        text = "Contact me at john.doe@example.com for more info."
        entities = model.predict_entities(text, ["email", "email address"], threshold=0.5)
        
        emails = [e["text"] for e in entities]
        assert any("john.doe@example.com" in email for email in emails)
    
    def test_extract_multiple_emails(self, model):
        text = "Send to alice@company.org or bob@company.org"
        entities = model.predict_entities(text, ["email", "email address"], threshold=0.5)
        
        assert len(entities) >= 2


class TestPhoneExtraction:
    """Test phone number extraction"""
    
    def test_extract_us_phone(self, model):
        text = "Call me at 555-123-4567 tomorrow."
        entities = model.predict_entities(text, ["phone number", "mobile phone number"], threshold=0.5)
        
        assert len(entities) >= 1
        phones = [e["text"] for e in entities]
        assert any("555-123-4567" in phone for phone in phones)
    
    def test_extract_international_phone(self, model):
        text = "His number is +1-800-555-0199"
        entities = model.predict_entities(text, ["phone number", "mobile phone number"], threshold=0.5)
        
        assert len(entities) >= 1


class TestSSNExtraction:
    """Test Social Security Number extraction"""
    
    def test_extract_ssn(self, model):
        text = "My SSN is 123-45-6789 for the application."
        entities = model.predict_entities(text, ["social security number"], threshold=0.5)
        
        assert len(entities) >= 1
        ssns = [e["text"] for e in entities]
        assert any("123-45-6789" in ssn for ssn in ssns)


class TestAddressExtraction:
    """Test address extraction"""
    
    def test_extract_address(self, model):
        text = "Ship the package to 123 Main Street, New York, NY 10001"
        entities = model.predict_entities(text, ["address"], threshold=0.5)
        
        assert len(entities) >= 1


class TestOrganizationExtraction:
    """Test organization name extraction"""
    
    def test_extract_organization(self, model):
        text = "She works at Microsoft Corporation in Seattle."
        entities = model.predict_entities(text, ["organization"], threshold=0.5)
        
        assert len(entities) >= 1
        orgs = [e["text"] for e in entities if e["label"] == "organization"]
        assert any("Microsoft" in org for org in orgs)


class TestMixedPIIExtraction:
    """Test extraction of multiple PII types from same text"""
    
    def test_extract_mixed_pii(self, model):
        text = """
        Patient: John Doe
        Email: john.doe@hospital.org
        Phone: (555) 987-6543
        SSN: 987-65-4321
        Address: 456 Oak Avenue, Boston, MA 02101
        """
        
        labels = ["person", "email", "phone number", "social security number", "address"]
        entities = model.predict_entities(text, labels, threshold=0.4)
        
        # Should extract at least 3 different entity types
        entity_types = set(e["label"] for e in entities)
        assert len(entity_types) >= 3
        
        # Check specific extractions
        texts = [e["text"] for e in entities]
        assert any("John Doe" in t for t in texts)
    
    def test_french_pii(self, model):
        """Test multilingual support - French"""
        text = "Jean Dupont habite au 15 Rue de la Paix, Paris. Son email est jean.dupont@mail.fr"
        
        labels = ["person", "email", "address"]
        entities = model.predict_entities(text, labels, threshold=0.4)
        
        assert len(entities) >= 1
        texts = [e["text"] for e in entities]
        # Should find at least the person or email
        assert any("Jean Dupont" in t or "jean.dupont@mail.fr" in t for t in texts)


class TestEntityMetadata:
    """Test that entity metadata is correctly returned"""
    
    def test_entity_has_required_fields(self, model):
        text = "Contact Alice at alice@test.com"
        entities = model.predict_entities(text, ["person", "email"], threshold=0.5)
        
        assert len(entities) >= 1
        for entity in entities:
            assert "text" in entity
            assert "label" in entity
            assert "start" in entity
            assert "end" in entity
            assert "score" in entity
    
    def test_entity_positions_are_valid(self, model):
        text = "John Smith works here."
        entities = model.predict_entities(text, ["person"], threshold=0.5)
        
        for entity in entities:
            start, end = entity["start"], entity["end"]
            assert start >= 0
            assert end <= len(text)
            assert start < end
            # Verify the extracted text matches the position
            assert text[start:end] == entity["text"]
    
    def test_confidence_score_range(self, model):
        text = "Email: test@example.com"
        entities = model.predict_entities(text, ["email"], threshold=0.3)
        
        for entity in entities:
            assert 0.0 <= entity["score"] <= 1.0


class TestThreshold:
    """Test threshold filtering"""
    
    def test_high_threshold_filters_entities(self, model):
        text = "Maybe contact john@test.com or call 555-1234"
        
        low_threshold = model.predict_entities(text, ["email", "phone number"], threshold=0.3)
        high_threshold = model.predict_entities(text, ["email", "phone number"], threshold=0.9)
        
        # High threshold should return same or fewer entities
        assert len(high_threshold) <= len(low_threshold)


class TestMultilingualParagraphs:
    """Test PII extraction from realistic paragraphs in multiple languages"""
    
    def test_english_paragraph(self, model):
        """Test extraction from a realistic English paragraph"""
        text = """
        Dear Customer Service,
        
        My name is Sarah Johnson and I am writing to report an issue with my recent order.
        I placed an order on December 10th, 2024 and have not received it yet. My order 
        confirmation was sent to sarah.johnson@gmail.com but I haven't received any shipping
        updates. You can reach me at (415) 555-8923 or at my home address: 
        742 Evergreen Terrace, Springfield, IL 62701.
        
        For reference, my account is linked to my SSN ending in 4532 and my driver's license
        number is D400-7891-2345. Please expedite the shipping to my work address at 
        TechCorp Industries, 100 Innovation Drive, Suite 500, San Francisco, CA 94105.
        
        Thank you for your assistance.
        
        Best regards,
        Sarah Johnson
        """
        
        labels = ["person", "email", "phone number", "address", "organization", 
                  "social security number", "driver's license number"]
        entities = model.predict_entities(text, labels, threshold=0.4)
        
        # Should find multiple entities
        assert len(entities) >= 3
        
        # Check for key entities
        texts = [e["text"].lower() for e in entities]
        labels_found = [e["label"] for e in entities]
        
        # Should find the person
        assert any("sarah johnson" in t for t in texts)
        # Should find the email
        assert any("sarah.johnson@gmail.com" in t for t in texts)
        # Should find at least one address or organization
        assert "address" in labels_found or "organization" in labels_found
    
    def test_french_paragraph(self, model):
        """Test extraction from a realistic French paragraph"""
        text = """
        Objet: Demande d'ouverture de compte bancaire
        
        Madame, Monsieur,
        
        Je soussigné, Pierre-Antoine Lefebvre, né le 15 mars 1985 à Lyon, souhaite 
        ouvrir un compte courant dans votre établissement. Je suis actuellement employé 
        chez Société Générale de Technologie à Paris.
        
        Vous pouvez me contacter par email à pierre.lefebvre@orange.fr ou par téléphone 
        au +33 6 12 34 56 78. Mon adresse actuelle est 25 Avenue des Champs-Élysées, 
        75008 Paris, France.
        
        Ci-joint les documents requis incluant ma carte d'identité numéro 123456789012
        et mon numéro de sécurité sociale 1 85 03 69 123 456 78.
        
        Dans l'attente de votre réponse, je vous prie d'agréer mes salutations distinguées.
        
        Pierre-Antoine Lefebvre
        """
        
        labels = ["person", "email", "phone number", "address", "organization",
                  "date of birth", "identity card number", "social security number"]
        entities = model.predict_entities(text, labels, threshold=0.4)
        
        # Should find multiple entities
        assert len(entities) >= 3
        
        # Check for key entities
        texts = [e["text"].lower() for e in entities]
        labels_found = [e["label"] for e in entities]
        
        # Should find the person name
        assert any("pierre" in t and "lefebvre" in t for t in texts)
        # Should find the email
        assert any("pierre.lefebvre@orange.fr" in t for t in texts)
        # Should find phone or address
        assert any(label in labels_found for label in ["phone number", "address", "mobile phone number"])
    
    def test_german_paragraph(self, model):
        """Test extraction from a realistic German paragraph"""
        text = """
        Betreff: Mietvertrag für Wohnung in München
        
        Sehr geehrte Damen und Herren,
        
        ich, Hans-Peter Müller, geboren am 22. Oktober 1978 in Berlin, möchte hiermit 
        mein Interesse an der Wohnung in der Maximilianstraße 45, 80539 München bekunden.
        
        Derzeit bin ich als Softwareentwickler bei BMW Group in München beschäftigt. 
        Mein monatliches Nettoeinkommen beträgt 4.500 Euro.
        
        Sie erreichen mich unter der E-Mail-Adresse hans.mueller@web.de oder telefonisch 
        unter +49 89 123 456 789. Meine aktuelle Adresse ist Berliner Straße 123, 
        10115 Berlin, Deutschland.
        
        Anbei finden Sie meinen Personalausweis mit der Nummer T220001293 sowie meine 
        Steuer-ID 12 345 678 901.
        
        Mit freundlichen Grüßen,
        Hans-Peter Müller
        """
        
        labels = ["person", "email", "phone number", "address", "organization",
                  "date of birth", "identity card number", "tax identification number"]
        entities = model.predict_entities(text, labels, threshold=0.4)
        
        # Should find multiple entities
        assert len(entities) >= 3
        
        # Check for key entities
        texts = [e["text"].lower() for e in entities]
        labels_found = [e["label"] for e in entities]
        
        # Should find the person name
        assert any("hans" in t and "müller" in t for t in texts) or any("muller" in t for t in texts)
        # Should find the email
        assert any("hans.mueller@web.de" in t for t in texts)
        # Should find organization
        assert any("bmw" in t for t in texts) or "organization" in labels_found
    
    def test_multilingual_entity_counts(self, model):
        """Verify all three languages extract comparable entity counts"""
        english_text = "Contact John Smith at john@email.com, phone 555-1234, address 123 Main St, New York"
        french_text = "Contacter Jean Dupont à jean@email.fr, téléphone 01 23 45 67 89, adresse 15 Rue de Paris"
        german_text = "Kontaktieren Sie Hans Schmidt unter hans@email.de, Telefon 030 12345678, Adresse Berliner Str. 10"
        
        labels = ["person", "email", "phone number", "address"]
        
        en_entities = model.predict_entities(english_text, labels, threshold=0.4)
        fr_entities = model.predict_entities(french_text, labels, threshold=0.4)
        de_entities = model.predict_entities(german_text, labels, threshold=0.4)
        
        # Each language should extract at least 2 entities
        assert len(en_entities) >= 2, f"English extracted only {len(en_entities)} entities"
        assert len(fr_entities) >= 2, f"French extracted only {len(fr_entities)} entities"
        assert len(de_entities) >= 2, f"German extracted only {len(de_entities)} entities"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
