from pathlib import Path

#Base Path
BASE_DIR = Path(__file__).resolve().parent
IO_DIR = BASE_DIR / "io"
IO_DIR.mkdir(parents=True, exist_ok=True)

#Datasets
CASES_DATA = IO_DIR / 'ALLARMI.csv'
PASSENGERS_DATA= IO_DIR / 'TIPOLOGIA_VIAGGIATORE.csv'

#Translation of columns
COLUMN_MAPPING_PASSENGERS = {
    'AREOPORTO_ARRIVO': 'arrival_airport_code',
    'AREOPORTO_PARTENZA': 'departure_airport_code',
    'ANNO_PARTENZA': 'departure_year',
    'MESE_PARTENZA': 'departure_month',
    'GIORNO_PARTENZA': 'departure_day',
    'DATA_PARTENZA': 'departure_date',
    'DESCR_AEREOPORTO_ARR': 'arrival_airport_name',
    'DESCR_AEREOPORTO_PART': 'departure_airport_name',
    'CITTA_ARR': 'arrival_city',
    'CITTA_PARTENZA': 'departure_city',
    'CODICE_PAESE_ARR': 'arrival_country_code',
    'CODICE_PAESE_PART': 'departure_country_code',
    'PAESE_ARR': 'arrival_country',
    'PAESE_PART': 'departure_country',
    'ZONA': 'zone',
    'ENTRATI': 'entries_count',
    'INVESTIGATI': 'investigated_count',
    'ALLARMATI': 'flagged_count',
    'GENERE': 'gender',
    'FLAG_TRANSITO': 'transit_flag',
    'ESITO_CONTROLLO': 'control_result',
    'note_operatore': 'operator_notes',
    'codice_rischio': 'risk_code',
    'Tipo Documento': 'document_type',
    'FASCIA ETA': 'age_range',
    '3nazionalita': 'nationality',
    'compagnia%aerea': 'airline',
    'num volo': 'flight_number'
}

GENDER_MAPPING = {
    'F': 'F', 'f': 'F', 'Femmina': 'F', 'Female': 'F', 'FEMALE': 'F', '2': 'F',
    'M': 'M', 'm': 'M', 'Maschio': 'M', 'Male': 'M', 'MALE': 'M', '1': 'M',
    'X': 'Other/NB', 'N/B': 'Other/NB'
}

COLUMN_MAPPING_CASES = {
    'OCCORRENZE': 'event_type',
    'AREOPORTO_ARRIVO': 'arrival_airport',
    'AREOPORTO_PARTENZA': 'departure_airport',
    'DATA_PARTENZA': 'departure_date',
    'DESCR_AEREOPORTO_ARR': 'arrival_airport_name',
    'CITTA_ARR': 'arrival_city',
    'CODICE_PAESE_ARR': 'arrival_country_code',
    'MOTIVO_ALLARME': 'alarm_reason',
    'note_operatore': 'operator_notes',
    'flag_rischio': 'risk_flag',
    'Paese Partenza': 'departure_country_name',
    'tot voli': 'total_flights'
}


#3 Alpha Country Codes
COUNTRY_MAPPING = {
    "Turchia": "TUR", "Regno Unito": "GBR", "Macedonia": "MKD", "North Macedonia": "MKD",
    "Qatar": "QAT", "Moldavia": "MDA", "Egitto": "EGY", "Arabia Saudita": "SAU",
    "Singapore": "SGP", "Italia": "ITA", "Armenia": "ARM", "Mauritius": "MUS",
    "Tunisia": "TUN", "Albania": "ALB", "Hong Kong": "HKG", "Marocco": "MAR",
    "Taiwan": "TWN", "Serbia": "SRB", "Oman": "OMN", "Algeria": "DZA",
    "Israele": "ISR", "Emirati Arabi Uniti": "ARE", "Corea del Sud": "KOR",
    "Iran": "IRN", "Maldive": "MDV", "Brasile": "BRA", "Cina": "CHN",
    "Giordania": "JOR", "Stati Uniti": "USA", "Etiopia": "ETH", "Argentina": "ARG",
    "Repubblica Dominicana": "DOM", "India": "IND", "Azerbaigian": "AZE",
    "Capo Verde": "CPV", "Tanzania": "TZA", "Senegal": "SEN", "Kuwait": "KWT",
    "Messico": "MEX", "Canada": "CAN", "Bahrain": "BHR", "Kenya": "KEN",
    "Montenegro": "MNE", "Libia": "LBY", "Cossovo": "XKX",
    "Libano": "LBN", "Georgia": "GEO", "Giappone": "JPN", "Uzbekistan": "UZB",
    "Kazakistan": "KAZ", "Antigua e Barbuda": "ATG", "Giamaica": "JAM"
}