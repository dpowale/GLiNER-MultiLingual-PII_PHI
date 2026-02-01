import json
import random

def generate_ner_dataset():
    languages = ["English", "French", "Spanish", "Portuguese", "Italian", "German"]
    
    dataset = []

    # Templates per language to ensure variety and label coverage - verbose sentences
    # Each language has multiple template groups to ensure comprehensive entity coverage
    templates = {
        "English": [
            # Employment & Contact
            "According to our company records, {person} is currently employed at {organization} with the employee identification number {student_id_number}, and their permanent residence is located at {address}. For any official correspondence, please use their registered email address {email_address}.",
            "The employee {person} from {organization} can be reached at their work email {email_address} or at the office address {address}. Their employee badge number is {student_id_number}.",
            "HR Department Notice: {person} has been assigned to {organization}. Contact information: email {email_address}, office location {address}, employee ID {student_id_number}.",
            
            # Medical Records
            "Medical Record Summary: The patient named {person}, whose date of birth is recorded as {date_of_birth}, was recently examined and subsequently diagnosed with {medical_condition}. Following the consultation, the attending physician prescribed {medication} as part of the treatment plan.",
            "Patient {person} (DOB: {date_of_birth}) presented with symptoms of {medical_condition}. Prescribed treatment: {medication}. Follow-up scheduled in two weeks.",
            "Clinical notes for {person}: Born {date_of_birth}, diagnosed condition: {medical_condition}, current prescription: {medication}. Patient responds well to treatment.",
            
            # Payment Processing
            "Payment Confirmation Notice: We are pleased to confirm that transaction number {transaction_number} has been successfully processed using a {credit_card_brand} card ending with the number {credit_card_number}. Please note that this card has an expiration date of {credit_card_expiration_date}.",
            "Receipt: Transaction {transaction_number} completed. Card type: {credit_card_brand}, Card number: {credit_card_number}, Expiry: {credit_card_expiration_date}, CVV verified: {credit_card_cvv}.",
            "Your order has been charged to your {credit_card_brand} card ({credit_card_number}). Transaction ID: {transaction_number}. Card expires {credit_card_expiration_date}. Security code {credit_card_cvv} was verified.",
            
            # Contact Information
            "For your reference, here are the contact details on file: the primary mobile phone number is {mobile_phone_number}, the fax machine can be reached at {fax_number}, and the individual can also be contacted through their social media handle {social_media_handle}.",
            "Contact directory entry: Mobile: {mobile_phone_number}, Fax: {fax_number}, Social media: {social_media_handle}, Landline: {landline_phone_number}.",
            "Updated contact info for record: Cell {mobile_phone_number}, Fax {fax_number}, Twitter/X handle {social_media_handle}.",
            
            # Travel Documents
            "Travel Itinerary Confirmation: The passenger {person} has been verified with passport number {passport_number}, which remains valid until the expiration date of {passport_expiration_date}. They are scheduled to depart on flight number {flight_number}.",
            "Boarding pass issued to {person}. Passport: {passport_number} (valid until {passport_expiration_date}). Flight: {flight_number}. Seat assignment confirmed.",
            "Immigration record: Traveler {person}, Passport No. {passport_number}, expiring {passport_expiration_date}, arrived on flight {flight_number}.",
            
            # Government IDs
            "Government Documentation Summary: The following official identification documents are on file - Social Security Number {social_security_number}, Tax Identification Number {tax_identification_number}, and National Identification Number {national_id_number}.",
            "Identity verification complete for {person}: SSN {social_security_number}, Tax ID {tax_identification_number}, National ID {national_id_number}.",
            "Official records show: SSN {social_security_number}, TIN {tax_identification_number}, Government ID {national_id_number} for the applicant.",
            
            # Vehicle Registration
            "Vehicle Registration Notice: The motor vehicle with license plate number {license_plate_number} and vehicle identification number {vehicle_registration_number} has been officially registered under the ownership of {organization}.",
            "DMV Record: Plate {license_plate_number}, VIN {vehicle_registration_number}, registered to {person} at {address}.",
            "Traffic citation: Vehicle with plate {license_plate_number} (VIN: {vehicle_registration_number}) owned by {organization}.",
            
            # Banking Details
            "Banking Information Statement: The complete banking details for the account holder {person} are as follows - International Bank Account Number {iban}, primary account number {bank_account_number}, and the card verification value is {credit_card_cvv}.",
            "Wire transfer details: Beneficiary {person}, IBAN: {iban}, Account: {bank_account_number}. Please include reference number in memo.",
            "Account verification for {person}: IBAN {iban}, Account number {bank_account_number}, Card CVV {credit_card_cvv}.",
            
            # Security & IT
            "Security Audit Log Entry: At the recorded timestamp, the user account {username} successfully authenticated and established a connection from IP address {ip_address}. The session was verified using digital signature {digital_signature}.",
            "Access log: User {username} logged in from {ip_address}. Session authenticated with signature {digital_signature}. Password last changed 30 days ago.",
            "IT Security Alert: Account {username} accessed from new IP {ip_address}. Digital signature {digital_signature} verified. No suspicious activity detected.",
            
            # Additional mixed templates
            "Customer profile: {person} from {organization}, email: {email_address}, phone: {mobile_phone_number}, SSN: {social_security_number}, address: {address}.",
            "Insurance claim submitted by {person} (DOB: {date_of_birth}, SSN: {social_security_number}) for treatment of {medical_condition} with {medication}.",
            "Reservation confirmation for {person}: Flight {flight_number}, Passport {passport_number}, Contact {email_address}, Phone {mobile_phone_number}."
        ],
        "French": [
            "Selon nos registres d'entreprise, {person} est actuellement employé chez {organization} avec le numéro d'identification d'employé {student_id_number}, et sa résidence permanente est située au {address}. Pour toute correspondance officielle, veuillez utiliser son adresse électronique enregistrée {email_address}.",
            "L'employé {person} de {organization} peut être joint à son email professionnel {email_address} ou à l'adresse du bureau {address}. Son numéro de badge est {student_id_number}.",
            "Avis RH: {person} a été affecté à {organization}. Coordonnées: email {email_address}, bureau {address}, ID employé {student_id_number}.",
            
            "Résumé du Dossier Médical: Le patient nommé {person}, dont la date de naissance est enregistrée comme étant le {date_of_birth}, a été récemment examiné et a ensuite été diagnostiqué avec {medical_condition}. Suite à la consultation, le médecin traitant a prescrit {medication} dans le cadre du plan de traitement.",
            "Patient {person} (né le {date_of_birth}) s'est présenté avec des symptômes de {medical_condition}. Traitement prescrit: {medication}. Suivi prévu dans deux semaines.",
            "Notes cliniques pour {person}: Né le {date_of_birth}, diagnostic: {medical_condition}, prescription actuelle: {medication}.",
            
            "Avis de Confirmation de Paiement: Nous avons le plaisir de confirmer que la transaction numéro {transaction_number} a été traitée avec succès en utilisant une carte {credit_card_brand} se terminant par le numéro {credit_card_number}. Veuillez noter que cette carte a une date d'expiration du {credit_card_expiration_date}.",
            "Reçu: Transaction {transaction_number} complétée. Type de carte: {credit_card_brand}, Numéro: {credit_card_number}, Expiration: {credit_card_expiration_date}, CVV vérifié: {credit_card_cvv}.",
            "Votre commande a été débitée sur votre carte {credit_card_brand} ({credit_card_number}). ID Transaction: {transaction_number}. Expiration {credit_card_expiration_date}. Code {credit_card_cvv} vérifié.",
            
            "Pour votre information, voici les coordonnées enregistrées: le numéro de téléphone mobile principal est {mobile_phone_number}, le télécopieur peut être joint au {fax_number}, et la personne peut également être contactée via son identifiant de réseau social {social_media_handle}.",
            "Annuaire: Mobile: {mobile_phone_number}, Fax: {fax_number}, Réseaux sociaux: {social_media_handle}, Fixe: {landline_phone_number}.",
            "Coordonnées mises à jour: Portable {mobile_phone_number}, Fax {fax_number}, Handle Twitter {social_media_handle}.",
            
            "Confirmation d'Itinéraire de Voyage: Le passager {person} a été vérifié avec le numéro de passeport {passport_number}, qui reste valide jusqu'à la date d'expiration du {passport_expiration_date}. Il est prévu de partir sur le vol numéro {flight_number}.",
            "Carte d'embarquement émise pour {person}. Passeport: {passport_number} (valide jusqu'au {passport_expiration_date}). Vol: {flight_number}.",
            "Registre d'immigration: Voyageur {person}, Passeport N° {passport_number}, expirant le {passport_expiration_date}, arrivé par vol {flight_number}.",
            
            "Résumé des Documents Gouvernementaux: Les documents d'identification officiels suivants sont en dossier - Numéro de Sécurité Sociale {social_security_number}, Numéro d'Identification Fiscale {tax_identification_number}, et Numéro d'Identification National {national_id_number}.",
            "Vérification d'identité complète pour {person}: NSS {social_security_number}, NIF {tax_identification_number}, ID National {national_id_number}.",
            "Dossiers officiels: NSS {social_security_number}, NIF {tax_identification_number}, ID Gouvernemental {national_id_number}.",
            
            "Avis d'Immatriculation de Véhicule: Le véhicule à moteur portant le numéro de plaque d'immatriculation {license_plate_number} et le numéro d'identification du véhicule {vehicle_registration_number} a été officiellement enregistré sous la propriété de {organization}.",
            "Certificat d'immatriculation: Plaque {license_plate_number}, NIV {vehicle_registration_number}, enregistré au nom de {person} au {address}.",
            "Procès-verbal: Véhicule immatriculé {license_plate_number} (NIV: {vehicle_registration_number}) appartenant à {organization}.",
            
            "Relevé d'Informations Bancaires: Les coordonnées bancaires complètes du titulaire du compte {person} sont les suivantes - Numéro de Compte Bancaire International {iban}, numéro de compte principal {bank_account_number}, et la valeur de vérification de la carte est {credit_card_cvv}.",
            "Détails de virement: Bénéficiaire {person}, IBAN: {iban}, Compte: {bank_account_number}.",
            "Vérification de compte pour {person}: IBAN {iban}, Numéro de compte {bank_account_number}, CVV {credit_card_cvv}.",
            
            "Entrée du Journal d'Audit de Sécurité: À l'horodatage enregistré, le compte utilisateur {username} s'est authentifié avec succès et a établi une connexion depuis l'adresse IP {ip_address}. La session a été vérifiée à l'aide de la signature numérique {digital_signature}.",
            "Journal d'accès: Utilisateur {username} connecté depuis {ip_address}. Signature {digital_signature} vérifiée.",
            "Alerte sécurité IT: Compte {username} accédé depuis nouvelle IP {ip_address}. Signature numérique {digital_signature} validée.",
            
            "Profil client: {person} de {organization}, email: {email_address}, téléphone: {mobile_phone_number}, NSS: {social_security_number}, adresse: {address}.",
            "Demande d'assurance soumise par {person} (né le {date_of_birth}, NSS: {social_security_number}) pour traitement de {medical_condition} avec {medication}.",
            "Confirmation de réservation pour {person}: Vol {flight_number}, Passeport {passport_number}, Contact {email_address}, Téléphone {mobile_phone_number}."
        ],
        "Spanish": [
            "Según nuestros registros de la empresa, {person} está actualmente empleado en {organization} con el número de identificación de empleado {student_id_number}, y su residencia permanente está ubicada en {address}. Para cualquier correspondencia oficial, por favor utilice su dirección de correo electrónico registrada {email_address}.",
            "El empleado {person} de {organization} puede ser contactado en su email laboral {email_address} o en la dirección de la oficina {address}. Su número de credencial es {student_id_number}.",
            "Aviso de RRHH: {person} ha sido asignado a {organization}. Contacto: email {email_address}, oficina {address}, ID de empleado {student_id_number}.",
            
            "Resumen del Expediente Médico: El paciente llamado {person}, cuya fecha de nacimiento está registrada como {date_of_birth}, fue examinado recientemente y posteriormente diagnosticado con {medical_condition}. Después de la consulta, el médico tratante recetó {medication} como parte del plan de tratamiento.",
            "Paciente {person} (nacido el {date_of_birth}) presentó síntomas de {medical_condition}. Tratamiento recetado: {medication}. Seguimiento programado en dos semanas.",
            "Notas clínicas para {person}: Nacido el {date_of_birth}, diagnóstico: {medical_condition}, prescripción actual: {medication}.",
            
            "Aviso de Confirmación de Pago: Nos complace confirmar que la transacción número {transaction_number} ha sido procesada exitosamente utilizando una tarjeta {credit_card_brand} que termina con el número {credit_card_number}. Por favor tenga en cuenta que esta tarjeta tiene una fecha de vencimiento del {credit_card_expiration_date}.",
            "Recibo: Transacción {transaction_number} completada. Tipo de tarjeta: {credit_card_brand}, Número: {credit_card_number}, Vencimiento: {credit_card_expiration_date}, CVV verificado: {credit_card_cvv}.",
            "Su pedido ha sido cargado a su tarjeta {credit_card_brand} ({credit_card_number}). ID de transacción: {transaction_number}. Vence {credit_card_expiration_date}. Código {credit_card_cvv} verificado.",
            
            "Para su referencia, aquí están los datos de contacto registrados: el número de teléfono móvil principal es {mobile_phone_number}, el fax puede ser contactado al {fax_number}, y la persona también puede ser contactada a través de su identificador de redes sociales {social_media_handle}.",
            "Directorio de contactos: Móvil: {mobile_phone_number}, Fax: {fax_number}, Redes sociales: {social_media_handle}, Fijo: {landline_phone_number}.",
            "Información de contacto actualizada: Celular {mobile_phone_number}, Fax {fax_number}, Handle de Twitter {social_media_handle}.",
            
            "Confirmación de Itinerario de Viaje: El pasajero {person} ha sido verificado con el número de pasaporte {passport_number}, que permanece válido hasta la fecha de vencimiento del {passport_expiration_date}. Está programado para partir en el vuelo número {flight_number}.",
            "Tarjeta de embarque emitida para {person}. Pasaporte: {passport_number} (válido hasta {passport_expiration_date}). Vuelo: {flight_number}.",
            "Registro de inmigración: Viajero {person}, Pasaporte N° {passport_number}, vence {passport_expiration_date}, llegó en vuelo {flight_number}.",
            
            "Resumen de Documentación Gubernamental: Los siguientes documentos de identificación oficial están en archivo - Número de Seguro Social {social_security_number}, Número de Identificación Fiscal {tax_identification_number}, y Número de Identificación Nacional {national_id_number}.",
            "Verificación de identidad completa para {person}: NSS {social_security_number}, NIF {tax_identification_number}, ID Nacional {national_id_number}.",
            "Registros oficiales: NSS {social_security_number}, NIF {tax_identification_number}, ID Gubernamental {national_id_number}.",
            
            "Aviso de Registro de Vehículo: El vehículo motorizado con número de placa {license_plate_number} y número de identificación del vehículo {vehicle_registration_number} ha sido oficialmente registrado bajo la propiedad de {organization}.",
            "Registro vehicular: Placa {license_plate_number}, NIV {vehicle_registration_number}, registrado a nombre de {person} en {address}.",
            "Infracción de tránsito: Vehículo con placa {license_plate_number} (NIV: {vehicle_registration_number}) propiedad de {organization}.",
            
            "Estado de Información Bancaria: Los datos bancarios completos del titular de la cuenta {person} son los siguientes - Número de Cuenta Bancaria Internacional {iban}, número de cuenta principal {bank_account_number}, y el valor de verificación de la tarjeta es {credit_card_cvv}.",
            "Detalles de transferencia: Beneficiario {person}, IBAN: {iban}, Cuenta: {bank_account_number}.",
            "Verificación de cuenta para {person}: IBAN {iban}, Número de cuenta {bank_account_number}, CVV {credit_card_cvv}.",
            
            "Entrada del Registro de Auditoría de Seguridad: En la marca de tiempo registrada, la cuenta de usuario {username} se autenticó exitosamente y estableció una conexión desde la dirección IP {ip_address}. La sesión fue verificada utilizando la firma digital {digital_signature}.",
            "Registro de acceso: Usuario {username} conectado desde {ip_address}. Firma {digital_signature} verificada.",
            "Alerta de seguridad TI: Cuenta {username} accedida desde nueva IP {ip_address}. Firma digital {digital_signature} validada.",
            
            "Perfil de cliente: {person} de {organization}, email: {email_address}, teléfono: {mobile_phone_number}, NSS: {social_security_number}, dirección: {address}.",
            "Reclamación de seguro presentada por {person} (nacido el {date_of_birth}, NSS: {social_security_number}) por tratamiento de {medical_condition} con {medication}.",
            "Confirmación de reserva para {person}: Vuelo {flight_number}, Pasaporte {passport_number}, Contacto {email_address}, Teléfono {mobile_phone_number}."
        ],
        "Portuguese": [
            "De acordo com nossos registros da empresa, {person} está atualmente empregado na {organization} com o número de identificação de funcionário {student_id_number}, e sua residência permanente está localizada em {address}. Para qualquer correspondência oficial, por favor use seu endereço de e-mail registrado {email_address}.",
            "O funcionário {person} da {organization} pode ser contatado em seu email de trabalho {email_address} ou no endereço do escritório {address}. Seu número de crachá é {student_id_number}.",
            "Aviso do RH: {person} foi designado para {organization}. Contato: email {email_address}, escritório {address}, ID de funcionário {student_id_number}.",
            
            "Resumo do Prontuário Médico: O paciente chamado {person}, cuja data de nascimento está registrada como {date_of_birth}, foi recentemente examinado e subsequentemente diagnosticado com {medical_condition}. Após a consulta, o médico assistente prescreveu {medication} como parte do plano de tratamento.",
            "Paciente {person} (nascido em {date_of_birth}) apresentou sintomas de {medical_condition}. Tratamento prescrito: {medication}. Acompanhamento agendado em duas semanas.",
            "Notas clínicas para {person}: Nascido em {date_of_birth}, diagnóstico: {medical_condition}, prescrição atual: {medication}.",
            
            "Aviso de Confirmação de Pagamento: Temos o prazer de confirmar que a transação número {transaction_number} foi processada com sucesso usando um cartão {credit_card_brand} terminando com o número {credit_card_number}. Por favor, observe que este cartão tem uma data de validade de {credit_card_expiration_date}.",
            "Recibo: Transação {transaction_number} concluída. Tipo de cartão: {credit_card_brand}, Número: {credit_card_number}, Validade: {credit_card_expiration_date}, CVV verificado: {credit_card_cvv}.",
            "Seu pedido foi cobrado no seu cartão {credit_card_brand} ({credit_card_number}). ID da transação: {transaction_number}. Vence em {credit_card_expiration_date}. Código {credit_card_cvv} verificado.",
            
            "Para sua referência, aqui estão os detalhes de contato registrados: o número de telefone celular principal é {mobile_phone_number}, o fax pode ser alcançado em {fax_number}, e a pessoa também pode ser contatada através de seu identificador de mídia social {social_media_handle}.",
            "Diretório de contatos: Celular: {mobile_phone_number}, Fax: {fax_number}, Redes sociais: {social_media_handle}, Fixo: {landline_phone_number}.",
            "Informações de contato atualizadas: Celular {mobile_phone_number}, Fax {fax_number}, Handle do Twitter {social_media_handle}.",
            
            "Confirmação de Itinerário de Viagem: O passageiro {person} foi verificado com o número de passaporte {passport_number}, que permanece válido até a data de validade de {passport_expiration_date}. Está programado para partir no voo número {flight_number}.",
            "Cartão de embarque emitido para {person}. Passaporte: {passport_number} (válido até {passport_expiration_date}). Voo: {flight_number}.",
            "Registro de imigração: Viajante {person}, Passaporte N° {passport_number}, vence em {passport_expiration_date}, chegou no voo {flight_number}.",
            
            "Resumo da Documentação Governamental: Os seguintes documentos de identificação oficial estão em arquivo - Número de Seguro Social {social_security_number}, Número de Identificação Fiscal {tax_identification_number}, e Número de Identificação Nacional {national_id_number}.",
            "Verificação de identidade completa para {person}: NSS {social_security_number}, NIF {tax_identification_number}, ID Nacional {national_id_number}.",
            "Registros oficiais: NSS {social_security_number}, NIF {tax_identification_number}, ID Governamental {national_id_number}.",
            
            "Aviso de Registro de Veículo: O veículo motorizado com número de placa {license_plate_number} e número de identificação do veículo {vehicle_registration_number} foi oficialmente registrado sob a propriedade da {organization}.",
            "Registro de veículo: Placa {license_plate_number}, VIN {vehicle_registration_number}, registrado em nome de {person} em {address}.",
            "Multa de trânsito: Veículo com placa {license_plate_number} (VIN: {vehicle_registration_number}) de propriedade de {organization}.",
            
            "Extrato de Informações Bancárias: Os detalhes bancários completos do titular da conta {person} são os seguintes - Número de Conta Bancária Internacional {iban}, número da conta principal {bank_account_number}, e o valor de verificação do cartão é {credit_card_cvv}.",
            "Detalhes da transferência: Beneficiário {person}, IBAN: {iban}, Conta: {bank_account_number}.",
            "Verificação de conta para {person}: IBAN {iban}, Número da conta {bank_account_number}, CVV {credit_card_cvv}.",
            
            "Entrada do Log de Auditoria de Segurança: No timestamp registrado, a conta de usuário {username} se autenticou com sucesso e estabeleceu uma conexão a partir do endereço IP {ip_address}. A sessão foi verificada usando a assinatura digital {digital_signature}.",
            "Log de acesso: Usuário {username} conectado de {ip_address}. Assinatura {digital_signature} verificada.",
            "Alerta de segurança TI: Conta {username} acessada de novo IP {ip_address}. Assinatura digital {digital_signature} validada.",
            
            "Perfil do cliente: {person} de {organization}, email: {email_address}, telefone: {mobile_phone_number}, NSS: {social_security_number}, endereço: {address}.",
            "Pedido de seguro apresentado por {person} (nascido em {date_of_birth}, NSS: {social_security_number}) para tratamento de {medical_condition} com {medication}.",
            "Confirmação de reserva para {person}: Voo {flight_number}, Passaporte {passport_number}, Contato {email_address}, Telefone {mobile_phone_number}."
        ],
        "Italian": [
            "Secondo i nostri registri aziendali, {person} è attualmente impiegato presso {organization} con il numero di identificazione dipendente {student_id_number}, e la sua residenza permanente si trova in {address}. Per qualsiasi corrispondenza ufficiale, si prega di utilizzare il suo indirizzo email registrato {email_address}.",
            "Il dipendente {person} di {organization} può essere contattato all'email aziendale {email_address} o all'indirizzo dell'ufficio {address}. Il suo numero di badge è {student_id_number}.",
            "Avviso HR: {person} è stato assegnato a {organization}. Contatti: email {email_address}, ufficio {address}, ID dipendente {student_id_number}.",
            
            "Riepilogo della Cartella Clinica: Il paziente di nome {person}, la cui data di nascita è registrata come {date_of_birth}, è stato recentemente esaminato e successivamente diagnosticato con {medical_condition}. A seguito della consultazione, il medico curante ha prescritto {medication} come parte del piano di trattamento.",
            "Paziente {person} (nato il {date_of_birth}) ha presentato sintomi di {medical_condition}. Trattamento prescritto: {medication}. Follow-up programmato tra due settimane.",
            "Note cliniche per {person}: Nato il {date_of_birth}, diagnosi: {medical_condition}, prescrizione attuale: {medication}.",
            
            "Avviso di Conferma del Pagamento: Siamo lieti di confermare che la transazione numero {transaction_number} è stata elaborata con successo utilizzando una carta {credit_card_brand} che termina con il numero {credit_card_number}. Si prega di notare che questa carta ha una data di scadenza del {credit_card_expiration_date}.",
            "Ricevuta: Transazione {transaction_number} completata. Tipo carta: {credit_card_brand}, Numero: {credit_card_number}, Scadenza: {credit_card_expiration_date}, CVV verificato: {credit_card_cvv}.",
            "Il suo ordine è stato addebitato sulla carta {credit_card_brand} ({credit_card_number}). ID transazione: {transaction_number}. Scade il {credit_card_expiration_date}. Codice {credit_card_cvv} verificato.",
            
            "Per vostro riferimento, ecco i dati di contatto registrati: il numero di cellulare principale è {mobile_phone_number}, il fax può essere raggiunto al {fax_number}, e la persona può anche essere contattata tramite il suo identificativo sui social media {social_media_handle}.",
            "Rubrica contatti: Cellulare: {mobile_phone_number}, Fax: {fax_number}, Social media: {social_media_handle}, Fisso: {landline_phone_number}.",
            "Informazioni di contatto aggiornate: Cellulare {mobile_phone_number}, Fax {fax_number}, Handle Twitter {social_media_handle}.",
            
            "Conferma dell'Itinerario di Viaggio: Il passeggero {person} è stato verificato con il numero di passaporto {passport_number}, che rimane valido fino alla data di scadenza del {passport_expiration_date}. È prevista la partenza sul volo numero {flight_number}.",
            "Carta d'imbarco emessa per {person}. Passaporto: {passport_number} (valido fino al {passport_expiration_date}). Volo: {flight_number}.",
            "Registro immigrazione: Viaggiatore {person}, Passaporto N° {passport_number}, scade il {passport_expiration_date}, arrivato con volo {flight_number}.",
            
            "Riepilogo della Documentazione Governativa: I seguenti documenti di identificazione ufficiali sono in archivio - Numero di Previdenza Sociale {social_security_number}, Numero di Identificazione Fiscale {tax_identification_number}, e Numero di Identificazione Nazionale {national_id_number}.",
            "Verifica identità completata per {person}: INPS {social_security_number}, Codice Fiscale {tax_identification_number}, ID Nazionale {national_id_number}.",
            "Registri ufficiali: INPS {social_security_number}, CF {tax_identification_number}, ID Governativo {national_id_number}.",
            
            "Avviso di Registrazione del Veicolo: Il veicolo a motore con numero di targa {license_plate_number} e numero di identificazione del veicolo {vehicle_registration_number} è stato ufficialmente registrato sotto la proprietà di {organization}.",
            "Libretto circolazione: Targa {license_plate_number}, VIN {vehicle_registration_number}, intestato a {person} in {address}.",
            "Verbale: Veicolo targato {license_plate_number} (VIN: {vehicle_registration_number}) di proprietà di {organization}.",
            
            "Estratto Conto delle Informazioni Bancarie: I dettagli bancari completi del titolare del conto {person} sono i seguenti - Numero di Conto Bancario Internazionale {iban}, numero di conto principale {bank_account_number}, e il valore di verifica della carta è {credit_card_cvv}.",
            "Dettagli bonifico: Beneficiario {person}, IBAN: {iban}, Conto: {bank_account_number}.",
            "Verifica conto per {person}: IBAN {iban}, Numero conto {bank_account_number}, CVV {credit_card_cvv}.",
            
            "Voce del Registro di Audit di Sicurezza: Al timestamp registrato, l'account utente {username} si è autenticato con successo e ha stabilito una connessione dall'indirizzo IP {ip_address}. La sessione è stata verificata utilizzando la firma digitale {digital_signature}.",
            "Log accesso: Utente {username} connesso da {ip_address}. Firma {digital_signature} verificata.",
            "Allarme sicurezza IT: Account {username} acceduto da nuovo IP {ip_address}. Firma digitale {digital_signature} validata.",
            
            "Profilo cliente: {person} di {organization}, email: {email_address}, telefono: {mobile_phone_number}, INPS: {social_security_number}, indirizzo: {address}.",
            "Richiesta assicurazione presentata da {person} (nato il {date_of_birth}, INPS: {social_security_number}) per trattamento di {medical_condition} con {medication}.",
            "Conferma prenotazione per {person}: Volo {flight_number}, Passaporto {passport_number}, Contatto {email_address}, Telefono {mobile_phone_number}."
        ],
        "German": [
            "Gemäß unseren Firmenunterlagen ist {person} derzeit bei {organization} mit der Mitarbeiteridentifikationsnummer {student_id_number} beschäftigt, und der ständige Wohnsitz befindet sich in {address}. Für jegliche offizielle Korrespondenz verwenden Sie bitte die registrierte E-Mail-Adresse {email_address}.",
            "Der Mitarbeiter {person} von {organization} kann unter der Arbeits-E-Mail {email_address} oder an der Büroadresse {address} erreicht werden. Seine Ausweisnummer ist {student_id_number}.",
            "HR-Mitteilung: {person} wurde {organization} zugewiesen. Kontakt: E-Mail {email_address}, Büro {address}, Mitarbeiter-ID {student_id_number}.",
            
            "Zusammenfassung der Krankenakte: Der Patient mit dem Namen {person}, dessen Geburtsdatum als {date_of_birth} erfasst ist, wurde kürzlich untersucht und anschließend mit {medical_condition} diagnostiziert. Nach der Konsultation verschrieb der behandelnde Arzt {medication} als Teil des Behandlungsplans.",
            "Patient {person} (geboren am {date_of_birth}) stellte sich mit Symptomen von {medical_condition} vor. Verschriebene Behandlung: {medication}. Nachkontrolle in zwei Wochen geplant.",
            "Klinische Notizen für {person}: Geboren am {date_of_birth}, Diagnose: {medical_condition}, aktuelle Verschreibung: {medication}.",
            
            "Zahlungsbestätigungsmitteilung: Wir freuen uns, Ihnen mitteilen zu können, dass die Transaktion Nummer {transaction_number} erfolgreich mit einer {credit_card_brand}-Karte mit der Nummer {credit_card_number} verarbeitet wurde. Bitte beachten Sie, dass diese Karte ein Ablaufdatum vom {credit_card_expiration_date} hat.",
            "Quittung: Transaktion {transaction_number} abgeschlossen. Kartentyp: {credit_card_brand}, Nummer: {credit_card_number}, Ablauf: {credit_card_expiration_date}, CVV verifiziert: {credit_card_cvv}.",
            "Ihre Bestellung wurde Ihrer {credit_card_brand}-Karte ({credit_card_number}) belastet. Transaktions-ID: {transaction_number}. Läuft ab am {credit_card_expiration_date}. Code {credit_card_cvv} verifiziert.",
            
            "Zu Ihrer Information sind hier die registrierten Kontaktdaten: Die primäre Mobiltelefonnummer ist {mobile_phone_number}, das Faxgerät ist erreichbar unter {fax_number}, und die Person kann auch über ihren Social-Media-Handle {social_media_handle} kontaktiert werden.",
            "Kontaktverzeichnis: Mobil: {mobile_phone_number}, Fax: {fax_number}, Social Media: {social_media_handle}, Festnetz: {landline_phone_number}.",
            "Aktualisierte Kontaktinformationen: Handy {mobile_phone_number}, Fax {fax_number}, Twitter-Handle {social_media_handle}.",
            
            "Reiserouten-Bestätigung: Der Passagier {person} wurde mit der Reisepassnummer {passport_number} verifiziert, der bis zum Ablaufdatum {passport_expiration_date} gültig bleibt. Der Abflug ist mit Flugnummer {flight_number} geplant.",
            "Bordkarte ausgestellt für {person}. Reisepass: {passport_number} (gültig bis {passport_expiration_date}). Flug: {flight_number}.",
            "Einreiseregister: Reisender {person}, Reisepass Nr. {passport_number}, läuft ab am {passport_expiration_date}, angekommen mit Flug {flight_number}.",
            
            "Zusammenfassung der Regierungsdokumente: Die folgenden offiziellen Ausweisdokumente liegen vor - Sozialversicherungsnummer {social_security_number}, Steueridentifikationsnummer {tax_identification_number}, und Nationale Identifikationsnummer {national_id_number}.",
            "Identitätsüberprüfung abgeschlossen für {person}: SVN {social_security_number}, Steuer-ID {tax_identification_number}, Nationale ID {national_id_number}.",
            "Offizielle Aufzeichnungen: SVN {social_security_number}, Steuer-ID {tax_identification_number}, Regierungs-ID {national_id_number}.",
            
            "Fahrzeugregistrierungsmitteilung: Das Kraftfahrzeug mit dem Kennzeichen {license_plate_number} und der Fahrzeugidentifikationsnummer {vehicle_registration_number} wurde offiziell unter dem Eigentum von {organization} registriert.",
            "Fahrzeugbrief: Kennzeichen {license_plate_number}, FIN {vehicle_registration_number}, zugelassen auf {person} in {address}.",
            "Strafzettel: Fahrzeug mit Kennzeichen {license_plate_number} (FIN: {vehicle_registration_number}) im Besitz von {organization}.",
            
            "Bankinformationsauszug: Die vollständigen Bankdaten des Kontoinhabers {person} lauten wie folgt - Internationale Bankkontonummer {iban}, Hauptkontonummer {bank_account_number}, und der Kartenprüfwert ist {credit_card_cvv}.",
            "Überweisungsdetails: Begünstigter {person}, IBAN: {iban}, Konto: {bank_account_number}.",
            "Kontoverifizierung für {person}: IBAN {iban}, Kontonummer {bank_account_number}, CVV {credit_card_cvv}.",
            
            "Sicherheits-Audit-Protokolleintrag: Zum erfassten Zeitstempel hat sich das Benutzerkonto {username} erfolgreich authentifiziert und eine Verbindung von der IP-Adresse {ip_address} hergestellt. Die Sitzung wurde mit der digitalen Signatur {digital_signature} verifiziert.",
            "Zugriffsprotokoll: Benutzer {username} angemeldet von {ip_address}. Signatur {digital_signature} verifiziert.",
            "IT-Sicherheitswarnung: Konto {username} von neuer IP {ip_address} zugegriffen. Digitale Signatur {digital_signature} validiert.",
            
            "Kundenprofil: {person} von {organization}, E-Mail: {email_address}, Telefon: {mobile_phone_number}, SVN: {social_security_number}, Adresse: {address}.",
            "Versicherungsanspruch eingereicht von {person} (geboren am {date_of_birth}, SVN: {social_security_number}) für Behandlung von {medical_condition} mit {medication}.",
            "Reservierungsbestätigung für {person}: Flug {flight_number}, Reisepass {passport_number}, Kontakt {email_address}, Telefon {mobile_phone_number}."
        ]
    }

    # Negative examples - sentences WITHOUT any PII/PHI entities (for testing false positives)
    # Expanded to 10 per language for better false positive testing
    negative_templates = {
        "English": [
            "The weather forecast for this weekend indicates partly cloudy skies with temperatures ranging between fifteen and twenty-two degrees Celsius. Light showers are expected on Sunday afternoon.",
            "Our quarterly report shows significant improvements in operational efficiency, with productivity increasing by twelve percent compared to the previous quarter. The team has implemented several new workflows.",
            "The museum exhibition features artwork from the Renaissance period, showcasing masterpieces from various European artists. Visitors can explore the gallery from nine in the morning until five in the evening.",
            "According to recent scientific studies, regular physical exercise combined with a balanced diet contributes significantly to overall health and well-being. Experts recommend at least thirty minutes of activity daily.",
            "The conference will focus on sustainable development practices and environmental conservation strategies. Keynote speakers will address topics related to renewable energy and carbon reduction initiatives.",
            "The new software update includes several bug fixes and performance improvements. Users are encouraged to restart their applications after the installation is complete.",
            "The restaurant offers a diverse menu featuring international cuisine prepared with locally sourced ingredients. Reservations are recommended for weekend dining.",
            "The library will be hosting a book club meeting every Thursday evening. Members are encouraged to read the selected novel before attending the discussion session.",
            "The hiking trail winds through ancient forests and offers spectacular views of the mountain range. The complete loop takes approximately four hours to finish.",
            "The documentary explores the history of space exploration and humanity's quest to understand the universe. It features interviews with leading astronomers and engineers."
        ],
        "French": [
            "Les prévisions météorologiques pour ce week-end indiquent un ciel partiellement nuageux avec des températures comprises entre quinze et vingt-deux degrés Celsius. De légères averses sont attendues dimanche après-midi.",
            "Notre rapport trimestriel montre des améliorations significatives de l'efficacité opérationnelle, avec une productivité en hausse de douze pour cent par rapport au trimestre précédent. L'équipe a mis en place plusieurs nouveaux processus.",
            "L'exposition du musée présente des œuvres d'art de la période de la Renaissance, mettant en valeur des chefs-d'œuvre de divers artistes européens. Les visiteurs peuvent explorer la galerie de neuf heures du matin à cinq heures du soir.",
            "Selon des études scientifiques récentes, l'exercice physique régulier combiné à une alimentation équilibrée contribue de manière significative à la santé et au bien-être général. Les experts recommandent au moins trente minutes d'activité quotidienne.",
            "La conférence se concentrera sur les pratiques de développement durable et les stratégies de conservation de l'environnement. Les conférenciers principaux aborderont des sujets liés aux énergies renouvelables et aux initiatives de réduction du carbone.",
            "La nouvelle mise à jour logicielle comprend plusieurs corrections de bugs et améliorations de performances. Les utilisateurs sont encouragés à redémarrer leurs applications après l'installation.",
            "Le restaurant propose un menu varié avec une cuisine internationale préparée avec des ingrédients locaux. Les réservations sont recommandées pour le week-end.",
            "La bibliothèque organisera une réunion du club de lecture chaque jeudi soir. Les membres sont encouragés à lire le roman sélectionné avant la discussion.",
            "Le sentier de randonnée serpente à travers des forêts anciennes et offre des vues spectaculaires sur la chaîne de montagnes. La boucle complète prend environ quatre heures.",
            "Le documentaire explore l'histoire de l'exploration spatiale et la quête de l'humanité pour comprendre l'univers. Il présente des entretiens avec des astronomes et des ingénieurs de premier plan."
        ],
        "Spanish": [
            "El pronóstico del tiempo para este fin de semana indica cielos parcialmente nublados con temperaturas que oscilan entre quince y veintidós grados Celsius. Se esperan lluvias ligeras el domingo por la tarde.",
            "Nuestro informe trimestral muestra mejoras significativas en la eficiencia operativa, con un aumento de la productividad del doce por ciento en comparación con el trimestre anterior. El equipo ha implementado varios flujos de trabajo nuevos.",
            "La exposición del museo presenta obras de arte del período del Renacimiento, mostrando obras maestras de diversos artistas europeos. Los visitantes pueden explorar la galería desde las nueve de la mañana hasta las cinco de la tarde.",
            "Según estudios científicos recientes, el ejercicio físico regular combinado con una dieta equilibrada contribuye significativamente a la salud y el bienestar general. Los expertos recomiendan al menos treinta minutos de actividad diaria.",
            "La conferencia se centrará en las prácticas de desarrollo sostenible y las estrategias de conservación ambiental. Los oradores principales abordarán temas relacionados con las energías renovables y las iniciativas de reducción de carbono.",
            "La nueva actualización de software incluye varias correcciones de errores y mejoras de rendimiento. Se recomienda a los usuarios reiniciar sus aplicaciones después de la instalación.",
            "El restaurante ofrece un menú diverso con cocina internacional preparada con ingredientes de origen local. Se recomiendan reservaciones para cenar el fin de semana.",
            "La biblioteca organizará una reunión del club de lectura todos los jueves por la noche. Se anima a los miembros a leer la novela seleccionada antes de asistir.",
            "El sendero de senderismo serpentea a través de bosques antiguos y ofrece vistas espectaculares de la cordillera. El circuito completo tarda aproximadamente cuatro horas.",
            "El documental explora la historia de la exploración espacial y la búsqueda de la humanidad para comprender el universo. Presenta entrevistas con astrónomos e ingenieros destacados."
        ],
        "Portuguese": [
            "A previsão do tempo para este fim de semana indica céu parcialmente nublado com temperaturas variando entre quinze e vinte e dois graus Celsius. Chuvas leves são esperadas no domingo à tarde.",
            "Nosso relatório trimestral mostra melhorias significativas na eficiência operacional, com a produtividade aumentando doze por cento em comparação com o trimestre anterior. A equipe implementou vários novos fluxos de trabalho.",
            "A exposição do museu apresenta obras de arte do período Renascentista, exibindo obras-primas de vários artistas europeus. Os visitantes podem explorar a galeria das nove da manhã às cinco da tarde.",
            "De acordo com estudos científicos recentes, o exercício físico regular combinado com uma dieta equilibrada contribui significativamente para a saúde e o bem-estar geral. Especialistas recomendam pelo menos trinta minutos de atividade diária.",
            "A conferência focará em práticas de desenvolvimento sustentável e estratégias de conservação ambiental. Os palestrantes principais abordarão tópicos relacionados a energia renovável e iniciativas de redução de carbono.",
            "A nova atualização de software inclui várias correções de bugs e melhorias de desempenho. Os usuários são encorajados a reiniciar seus aplicativos após a instalação.",
            "O restaurante oferece um menu diversificado com culinária internacional preparada com ingredientes de origem local. Reservas são recomendadas para jantar no fim de semana.",
            "A biblioteca organizará uma reunião do clube do livro toda quinta-feira à noite. Os membros são encorajados a ler o romance selecionado antes de participar.",
            "A trilha de caminhada serpenteia através de florestas antigas e oferece vistas espetaculares da cordilheira. O circuito completo leva aproximadamente quatro horas.",
            "O documentário explora a história da exploração espacial e a busca da humanidade para entender o universo. Apresenta entrevistas com astrônomos e engenheiros de destaque."
        ],
        "Italian": [
            "Le previsioni meteo per questo fine settimana indicano cieli parzialmente nuvolosi con temperature comprese tra quindici e ventidue gradi Celsius. Sono previste leggere piogge domenica pomeriggio.",
            "Il nostro rapporto trimestrale mostra miglioramenti significativi nell'efficienza operativa, con la produttività in aumento del dodici per cento rispetto al trimestre precedente. Il team ha implementato diversi nuovi flussi di lavoro.",
            "La mostra del museo presenta opere d'arte del periodo rinascimentale, esponendo capolavori di vari artisti europei. I visitatori possono esplorare la galleria dalle nove del mattino alle cinque del pomeriggio.",
            "Secondo recenti studi scientifici, l'esercizio fisico regolare combinato con una dieta equilibrata contribuisce significativamente alla salute e al benessere generale. Gli esperti raccomandano almeno trenta minuti di attività quotidiana.",
            "La conferenza si concentrerà sulle pratiche di sviluppo sostenibile e sulle strategie di conservazione ambientale. I relatori principali affronteranno argomenti relativi alle energie rinnovabili e alle iniziative di riduzione del carbonio.",
            "Il nuovo aggiornamento software include diverse correzioni di bug e miglioramenti delle prestazioni. Gli utenti sono incoraggiati a riavviare le loro applicazioni dopo l'installazione.",
            "Il ristorante offre un menu diversificato con cucina internazionale preparata con ingredienti di provenienza locale. Le prenotazioni sono consigliate per il fine settimana.",
            "La biblioteca ospiterà un incontro del club del libro ogni giovedì sera. I membri sono incoraggiati a leggere il romanzo selezionato prima di partecipare.",
            "Il sentiero escursionistico si snoda attraverso foreste antiche e offre viste spettacolari sulla catena montuosa. Il circuito completo richiede circa quattro ore.",
            "Il documentario esplora la storia dell'esplorazione spaziale e la ricerca dell'umanità per comprendere l'universo. Presenta interviste con astronomi e ingegneri di spicco."
        ],
        "German": [
            "Die Wettervorhersage für dieses Wochenende zeigt teilweise bewölkten Himmel mit Temperaturen zwischen fünfzehn und zweiundzwanzig Grad Celsius. Am Sonntagnachmittag werden leichte Schauer erwartet.",
            "Unser Quartalsbericht zeigt deutliche Verbesserungen der betrieblichen Effizienz, wobei die Produktivität im Vergleich zum Vorquartal um zwölf Prozent gestiegen ist. Das Team hat mehrere neue Arbeitsabläufe eingeführt.",
            "Die Museumsausstellung zeigt Kunstwerke aus der Renaissance und präsentiert Meisterwerke verschiedener europäischer Künstler. Besucher können die Galerie von neun Uhr morgens bis fünf Uhr abends erkunden.",
            "Laut aktuellen wissenschaftlichen Studien trägt regelmäßige körperliche Bewegung in Kombination mit einer ausgewogenen Ernährung wesentlich zur allgemeinen Gesundheit und zum Wohlbefinden bei. Experten empfehlen mindestens dreißig Minuten Aktivität täglich.",
            "Die Konferenz wird sich auf nachhaltige Entwicklungspraktiken und Umweltschutzstrategien konzentrieren. Die Hauptredner werden Themen im Zusammenhang mit erneuerbaren Energien und Kohlenstoffreduktionsinitiativen behandeln.",
            "Das neue Software-Update enthält mehrere Fehlerbehebungen und Leistungsverbesserungen. Benutzer werden ermutigt, ihre Anwendungen nach der Installation neu zu starten.",
            "Das Restaurant bietet ein vielfältiges Menü mit internationaler Küche aus regionalen Zutaten. Reservierungen werden für das Wochenende empfohlen.",
            "Die Bibliothek veranstaltet jeden Donnerstagabend ein Treffen des Buchclubs. Mitglieder werden ermutigt, den ausgewählten Roman vor der Diskussion zu lesen.",
            "Der Wanderweg führt durch alte Wälder und bietet spektakuläre Aussichten auf die Bergkette. Die komplette Runde dauert etwa vier Stunden.",
            "Der Dokumentarfilm erforscht die Geschichte der Raumfahrt und die Suche der Menschheit nach dem Verständnis des Universums. Er enthält Interviews mit führenden Astronomen und Ingenieuren."
        ]
    }

    # Data pools for randomization per language
    person_names = {
        "English": ["John Doe", "Jane Smith", "Robert Johnson", "Emily Davis", "Michael Brown", "Sarah Wilson"],
        "French": ["Marie Curie", "Jean Dupont", "Pierre Martin", "Sophie Bernard", "Luc Moreau", "Claire Dubois"],
        "Spanish": ["Juan Carlos", "Maria Garcia", "Carlos Lopez", "Ana Martinez", "Pedro Sanchez", "Laura Fernandez"],
        "Portuguese": ["Ana Silva", "João Santos", "Maria Oliveira", "Pedro Costa", "Carla Pereira", "Bruno Ferreira"],
        "Italian": ["Mario Rossi", "Giulia Bianchi", "Luca Ferrari", "Francesca Romano", "Marco Colombo", "Elena Ricci"],
        "German": ["Hans Müller", "Anna Schmidt", "Klaus Weber", "Petra Fischer", "Wolfgang Braun", "Ingrid Hoffmann"]
    }
    
    organizations = ["GlobalCorp Industries", "TechVision Ltd", "MediHealth Solutions", "EuroFinance AG", 
                     "DataSystems Inc", "GreenEnergy Corp", "SmartLogistics GmbH", "CloudNet Services"]
    
    addresses = {
        "English": ["123 Main St, New York", "456 Oak Ave, Los Angeles", "789 Elm Rd, Chicago", "321 Pine Ln, Boston"],
        "French": ["12 Rue de Paris, Lyon", "34 Avenue Montaigne, Paris", "56 Boulevard Saint-Michel, Marseille"],
        "Spanish": ["Calle Mayor 15, Madrid", "Paseo de Gracia 42, Barcelona", "Avenida Libertad 78, Valencia"],
        "Portuguese": ["Rua Augusta 100, Lisboa", "Av. Paulista 500, São Paulo", "Rua das Flores 25, Porto"],
        "Italian": ["Via Roma 10, Milano", "Piazza Navona 5, Roma", "Corso Italia 30, Firenze"],
        "German": ["Hauptstraße 20, Berlin", "Königsallee 15, München", "Bahnhofstraße 8, Frankfurt"]
    }
    
    medical_conditions = ["Diabetes Type 2", "Hypertension", "Asthma", "Arthritis", "Migraine", "Allergies"]
    medications = ["Metformin", "Lisinopril", "Albuterol", "Ibuprofen", "Sumatriptan", "Cetirizine"]
    credit_card_brands = ["Mastercard", "Visa", "American Express", "Discover"]
    flight_codes = ["LH", "AF", "BA", "IB", "AA", "DL", "UA", "EK"]
    
    def random_phone():
        return f"+{random.randint(1,49)}-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    
    def random_email(name):
        domains = ["example.com", "mail.org", "test.net", "company.io"]
        clean_name = name.lower().replace(" ", ".").replace("ü", "u").replace("ä", "a").replace("ö", "o")
        return f"{clean_name}{random.randint(1,99)}@{random.choice(domains)}"
    
    def random_date():
        return f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{random.randint(1950,2005)}"
    
    def random_cc_number():
        return f"{random.randint(4000,5999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    
    def random_exp_date():
        return f"{random.randint(1,12):02d}/{random.randint(25,32)}"
    
    def random_passport():
        return f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10000000,99999999)}"
    
    def random_ssn():
        return f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
    
    def random_ip():
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

    for lang in languages:
        # Increased from 20 to 50 positive samples per language for better coverage
        for i in range(50):
            template = templates[lang][i % len(templates[lang])]  # Cycle through all templates
            person = random.choice(person_names[lang])
            
            # Synthetic Data Injectors with randomization
            data = {
                "person": person,
                "organization": random.choice(organizations),
                "address": random.choice(addresses[lang]),
                "email_address": random_email(person),
                "date_of_birth": random_date(),
                "medical_condition": random.choice(medical_conditions),
                "medication": random.choice(medications),
                "transaction_number": f"TRX-{random.randint(100000,999999)}",
                "credit_card_brand": random.choice(credit_card_brands),
                "credit_card_number": random_cc_number(),
                "credit_card_expiration_date": random_exp_date(),
                "mobile_phone_number": random_phone(),
                "fax_number": random_phone(),
                "landline_phone_number": f"+{random.randint(1,49)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
                "social_media_handle": f"@{person.split()[0].lower()}{random.randint(1,999)}",
                "passport_number": random_passport(),
                "passport_expiration_date": f"{random.randint(2026,2035)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "flight_number": f"{random.choice(flight_codes)}{random.randint(100,9999)}",
                "social_security_number": random_ssn(),
                "tax_identification_number": f"TIN{random.randint(100000,999999)}",
                "national_id_number": f"ID-{random.randint(100000,999999)}",
                "license_plate_number": f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}-{random.randint(1000,9999)}",
                "vehicle_registration_number": f"VIN-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100,999)}",
                "iban": f"{random.choice(['DE','FR','ES','IT','PT','GB'])}{random.randint(10,99)} {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(10,99)}",
                "bank_account_number": f"{random.randint(1000000000,9999999999)}",
                "credit_card_cvv": f"{random.randint(100,999)}",
                "username": f"{person.split()[0].lower()}_{random.randint(1,999)}",
                "ip_address": random_ip(),
                "digital_signature": f"SIG-{random.randint(100000,999999)}",
                "student_id_number": f"SID-{random.randint(1000,9999)}"
            }

            # Fill template with all values first
            text = template
            for key, value in data.items():
                text = text.replace(f"{{{key}}}", value)
            
            # Now find entity positions in the final text
            entities = []
            for key, value in data.items():
                if f"{{{key}}}" in template:  # Check if this key was in the original template
                    start_idx = text.find(value)
                    if start_idx != -1:
                        entities.append({
                            "text": value,
                            "label": key,  # Keep underscore format for consistency
                            "start": start_idx,
                            "end": start_idx + len(value)
                        })
            
            dataset.append({
                "language": lang,
                "text": text,
                "entities": entities
            })
    
    # Add negative examples (sentences without PII) for each language
    for lang in languages:
        for neg_template in negative_templates[lang]:
            dataset.append({
                "language": lang,
                "text": neg_template,
                "entities": []  # Empty entities - no PII in these sentences
            })

    # Shuffle the dataset to mix positive and negative examples
    random.shuffle(dataset)
    
    total_positive = sum(1 for d in dataset if len(d["entities"]) > 0)
    total_negative = sum(1 for d in dataset if len(d["entities"]) == 0)

    with open('ner_evaluation_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    return f"File 'ner_evaluation_dataset.json' created with {len(dataset)} entries ({total_positive} positive, {total_negative} negative)."

# Execute
print(generate_ner_dataset())
