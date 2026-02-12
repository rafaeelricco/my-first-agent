from datetime import date

unidas_extract_prompt = f"""
Use Playwright MCP server to extract car rental pricing from https://www.unidas.com.br/para-voce/reservas-nacionais:

## Inputs
- **Pickup location:** Aeroporto de Porto Alegre, Porto Alegre (might we need to delete some words to trigger the location autocomplete)
- **Pickup date:** {date.today().replace(day=23).strftime("%d/%m/%Y")} at 10:00 AM
- **Return date:** 30 days after pickup
- **Vehicle group:** SUV Compacto
- **Mileage:** 1,000 Km
- **Protection:** Proteção Parcial (Partial Protection)

## IMPORTANT WORKAROUND
The website has a bug where protection displays incorrect values when preselected. You MUST:

1. First select "Proteção Completa"
2. Then switch to "Proteção Parcial"

## Instructions
1. Use the Playwright MCP server to navigate and extract pricing.
2. Extract and record:
   - daily rate
   - total rental days
   - protection cost
   - administrative fee
   - final total amount
3. Format the summary clearly with all pricing breakdowns.
"""

unidas_extract_expected_output = """
Precos de aluguel de carro da Unidas extraidos:
- Veiculo: <grupo do veiculo e quilometragem>
- Datas: <data_inicial> ate 30 dias depois
- Diaria: R$ <valor_diaria>
- Protecao (Parcial): R$ <valor_protecao_por_dia>/dia (Total R$ <valor_total_protecao>)
- Taxa administrativa (15%): R$ <valor_taxa_administrativa>
- Total final: R$ <valor_total_final>
"""
