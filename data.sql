CREATE TABLE data (
  url TEXT NOT NULL,
  get_date TEXT DEFAULT NULL,
  page_status TEXT DEFAULT NULL,
  directory TEXT DEFAULT NULL,
  cod TEXT DEFAULT NULL,
  status TEXT DEFAULT NULL,
  last_status TEXT DEFAULT NULL,
  last_update TEXT DEFAULT NULL,
  Dati_relativi_al_lotto_description text,
  Dati_relativi_al_lotto_INDIRIZZO TEXT DEFAULT NULL,
  Dati_relativi_al_lotto_LOTTO TEXT DEFAULT NULL,
  Dati_relativi_al_lotto_NUMERO_BENI TEXT DEFAULT NULL,
  Dati_relativi_al_lotto_GENERE TEXT DEFAULT NULL,
  Dati_relativi_al_lotto_CATEGORIA TEXT DEFAULT NULL,
  Dati_relativi_al_lotto_VALORE_DI_STIMA TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_tipo TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_description text,
  Dati_relativi_ai_beni_INDIRIZZO TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_PIANO TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_DISPONIBILITÀ TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_VANI TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_METRI_QUADRI TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_METRI_QUADRI_MIN float DEFAULT NULL,
  Dati_relativi_ai_beni_METRI_QUADRI_MAX float DEFAULT NULL,
  Dati_relativi_ai_beni_CERTIFICAZIONE_ENERGETICA TEXT DEFAULT NULL,
  Dati_relativi_ai_beni_DATI_CATASTALI TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_DATA_E_ORA_UDIENZA datetime DEFAULT NULL,
  Dati_relativi_alla_Vendita_DATA_E_ORA_VENDITA TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_TIPO_VENDITA TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_MODALITA_VENDITA TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_LUOGO_DELLA_VENDITA TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_LUOGO_PRESENTAZIONE_OFFERTA TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_TERMINE_PRESENTAZIONE_OFFERTE datetime DEFAULT NULL,
  Dati_relativi_alla_Vendita_PREZZO_BASE float DEFAULT NULL,
  Dati_relativi_alla_Vendita_OFFERTA_MINIMA float DEFAULT NULL,
  Dati_relativi_alla_Vendita_RIALZO_MINIMO_IN_CASO_DI_GARA float DEFAULT NULL,
  Dati_relativi_alla_Vendita_DEPOSITO_CAUZIONALE TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_DEPOSITO_IN_CONTO_SPESE TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_DATA_INIZIO_GARA TEXT DEFAULT NULL,
  Dati_relativi_alla_Vendita_DATA_FINE_GARA TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_TRIBUNALE TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_TIPO_PROCEDURA TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_RUOLO TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_RUOLO_1 int DEFAULT NULL,
  Dettaglio_procedura_e_contatti_RUOLO_2 int DEFAULT NULL,
  Numero_dei_Creditori int DEFAULT NULL,
  Dettaglio_procedura_e_contatti_DELEGATO_ALLA_VENDITA TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_RECAPITI TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_EMAIL TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_CUSTODE_GIUDIZIARIO TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_GIUDICE TEXT DEFAULT NULL,
  Dettaglio_procedura_e_contatti_IVG TEXT DEFAULT NULL,
  zip TEXT DEFAULT NULL,
  PRIMARY KEY (`url`))
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
