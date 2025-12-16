#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clasificador de Temas para Comentarios de Campañas
Personalizable por campaña/producto
"""
import re
from typing import Callable

def create_topic_classifier_v2() -> Callable[[str], str]:
    """
    Clasificador v2: Optimizado para campaña de Avena Canela Navidad.
    Incluye detección de Influencers, Spam agresivo y matices de ingredientes.
    """

    def classify_topic(comment: str) -> str:
        # Convertir a minúsculas y limpiar espacios extra
        comment_lower = str(comment).lower().strip()
        
        # ---------------------------------------------------------
        # CATEGORÍA 1: Ingredientes, Salud y Críticas Físicas
        # (Prioridad alta: incluye términos técnicos detectados)
        # ---------------------------------------------------------
        if re.search(
            r'carragenina|espesante|qu[ií]mico|cancer[ií]gen|'  # Nuevo detectado
            r'conservantes|preservantes|aditivos|saludable|'
            r'az[uú]car|dulce|diabetes|baja.*az[uú]car|'
            r'ingredientes|lactosa|sabor a remedio',            # Nuevo detectado
            comment_lower
        ):
            return 'Ingredientes y Salud'

        # ---------------------------------------------------------
        # CATEGORÍA 2: Competencia (Marca vs Marca)
        # ---------------------------------------------------------
        if re.search(
            r'avena torres|torres g[oó]mez|colanta|alpina vs|mejor que la avena|'
            r'otra marca|competencia|marca\s+\w+|queremos a torres',
            comment_lower
        ):
            return 'Competencia / Comparación'

        # ---------------------------------------------------------
        # CATEGORÍA 3: Talento, Influencers y el Video (NUEVA)
        # ---------------------------------------------------------
        # Detecta menciones a "Chris", "Vale", y saludos al video
        if re.search(
            r'chris|vale\b|valeria|haces ah[ií]|verte en|saludo|'
            r'anuncio|publicidad|comercial|video|actriz|actor',
            comment_lower
        ):
            return 'Talento e Influencers'

        # ---------------------------------------------------------
        # CATEGORÍA 4: Preguntas y Disponibilidad
        # ---------------------------------------------------------
        if re.search(
            r'precio|vale\?|d[oó]nde.*queda|d[oó]nde.*comprar|'
            r'c[oó]mo consigo|disponible|tiendas|sopo|' # Sopo agregado por el comentario de la tienda
            r'visite la tienda|ubicaci[oó]n',
            comment_lower
        ):
            return 'Preguntas / Puntos de Venta'

        # ---------------------------------------------------------
        # CATEGORÍA 5: Opinión Positiva / Brand Love
        # ---------------------------------------------------------
        # Movemos esto ANTES del filtro de longitud para capturar "Deli"
        if re.search(
            r'deli\b|rico|delicios|encanta|bueno|espectacular|'
            r'gusta|am[oó] este|fan|top|combina|paraiso|' 
            r'excelente|buen producto',
            comment_lower
        ):
            return 'Opinión Positiva / Brand Love'
            
        # ---------------------------------------------------------
        # CATEGORÍA 6: Spam y Conversación Irrelevante (NUEVO FILTRO)
        # ---------------------------------------------------------
        # Captura las conversaciones raras de tu dataset
        if re.search(
            r'am[eé]n|dios|jes[uú]s|bendiga|bendiciones|'  # Religioso
            r'ucrania|neos|rusia|c[aá]rcel|basura|polic[ií]a|' # Política/Social
            r'brandon|sofia|julio|larin|pap[aá]|padres|'   # Nombres random del chat
            r'hpta|maldit|caca|pudran',                    # Insultos random
            comment_lower
        ):
            return 'Spam / Fuera de Tema'

        # ---------------------------------------------------------
        # CATEGORÍA 7: Solo Emojis / Muy cortos sin contexto
        # ---------------------------------------------------------
        # Si no cayó en opiniones (como "deli"), y es muy corto, va aquí.
        if len(comment_lower.split()) < 2: 
            # Detectar si son solo caracteres no alfanuméricos (emojis, signos)
            if not re.search(r'[a-z]', comment_lower):
                return 'Reacción (Solo Emojis)'
            return 'Indeterminado (Muy corto)'

        # ---------------------------------------------------------
        # DEFAULT
        # ---------------------------------------------------------
        return 'Otros'

    return classify_topic

# ============================================================================
# METADATA DE LA CAMPAÑA (OPCIONAL)
# ============================================================================

CAMPAIGN_METADATA = {
    'campaign_name': 'Alpina - Kéfir',
    'product': 'Kéfir Alpina',
    'categories': [
        'Preguntas sobre el Producto',
        'Comparación con Kéfir Casero/Artesanal',
        'Ingredientes y Salud',
        'Competencia y Disponibilidad',
        'Opinión General del Producto',
        'Fuera de Tema / No Relevante',
        'Otros'
    ],
    'version': '1.0',
    'last_updated': '2025-11-20'
}


def get_campaign_metadata() -> dict:
    """Retorna metadata de la campaña"""
    return CAMPAIGN_METADATA.copy()
