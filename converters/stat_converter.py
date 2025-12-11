import csv

def format_number(num_str):
    return num_str.strip()

def parse_csv_to_template(csv_text):
    lines = csv_text.strip().split('\n')
    reader = csv.reader(lines)
    rows = list(reader)
    
    column_header_row = None
    for i, row in enumerate(rows):
        if any('Upgrade #' in str(cell) for cell in row):
            column_header_row = i
            break
    
    if column_header_row is None:
        return "column header not found"
    
    header_row = rows[column_header_row]
    unit_starts = []
    
    for i, cell in enumerate(header_row):
        if 'Upgrade #' in str(cell):
            unit_starts.append(i)
    
    valid_unit_data = None
    
    for unit_idx, start_col in enumerate(unit_starts):
        end_col = unit_starts[unit_idx + 1] if unit_idx + 1 < len(unit_starts) else len(header_row)
        
        headers = []
        for col_idx in range(start_col, end_col):
            if col_idx < len(header_row):
                header = str(header_row[col_idx]).strip()
                if header:
                    headers.append((col_idx, header))
        
        upgrades = []
        for row_idx in range(column_header_row + 1, len(rows)):
            row = rows[row_idx]
            
            upgrade = {}
            for col_idx, header in headers:
                if col_idx < len(row):
                    value = str(row[col_idx]).strip()
                    if value:
                        upgrade[header] = value
            
            if 'Upgrade #' in upgrade and 'Cost' in upgrade:
                cost = upgrade.get('Cost', '').replace(' ', '').replace(',', '')
                if cost and cost != '0' and cost != '':
                    upgrades.append(upgrade)
        
        if upgrades and valid_unit_data is None:
            valid_unit_data = upgrades
            break
    
    if not valid_unit_data:
        return "unit data not found. did you input it?"
    
    result = ["{{Main Stats Outer Shell|"]
    
    previous_aoe = None
    
    for upgrade in valid_unit_data:
        damage = upgrade.get('Damage', '').replace(',', '').replace(' ', '')
        if damage == '0' or damage == '':
            continue
        
        parts = ["{{Stats Box"]
        extra_lines = []
        
        if 'Cost' in upgrade:
            cost = format_number(upgrade['Cost'])
            parts.append(f"|Upgrade_Cost={cost}")
        
        if 'Upgrade #' in upgrade:
            parts.append(f"|Upgrade_No={upgrade['Upgrade #']}")
        
        if 'Damage' in upgrade:
            damage_val = format_number(upgrade['Damage'])
            if damage_val and damage_val != '0':
                parts.append(f"|Damage={damage_val}")
        
        if 'Range' in upgrade and upgrade['Range']:
            parts.append(f"|Range={upgrade['Range']}")
        
        if 'SPA' in upgrade and upgrade['SPA']:
            parts.append(f"|SPA={upgrade['SPA']}")
        
        has_attack_name = 'Attack Name' in upgrade and upgrade['Attack Name']
        
        if has_attack_name:
            extra_lines.append(f"|Tower_Type={upgrade.get('Tower Type', 'Hybrid')} ")
            
            current_aoe = upgrade.get('AoE Type', '')
            extra_lines.append(f"|Attack_Type=AoE ({current_aoe})")
            
            extra_lines.append(f"|Text_Line_1='''{upgrade['Attack Name']}'''")
            
            status_effects = []
            i = 1
            while f'Status Effect {i}' in upgrade and upgrade[f'Status Effect {i}']:
                status_effects.append(upgrade[f'Status Effect {i}'])
                i += 1
            
            if status_effects:
                status_text = "Attacks inflict " + " and ".join([f"{{{{Passive|{s}}}}}" for s in status_effects])
                extra_lines.append(f"|Text_Line_2='''{status_text}'''")
            
            if previous_aoe and previous_aoe != current_aoe:
                extra_lines.append(f"|AoE_Change=AoE ({current_aoe})")
            
            previous_aoe = current_aoe
        
        if extra_lines:
            result.append(''.join(parts))
            result.extend(extra_lines)
            result.append("}}")
        else:
            result.append(''.join(parts) + "}}")
    
    result.append("}}")
    
    return '\n'.join(result)