def format_wheel_order(fitment, summary):
    summary_parts = summary.split("|")
    wheel_series = summary_parts[1].strip() if len(summary_parts) > 1 else ""
    is_monoblock = "-M" in wheel_series.upper()
    is_ecl = "ECL" in wheel_series.upper()

    if is_monoblock and len(summary_parts) < 4:
        raise ValueError("Monoblock summary must have 4 parts: VEHICLE | SERIES | CENTER FINISH | CAPS")
    if not is_monoblock and not is_ecl and len(summary_parts) < 7:
        raise ValueError("3-piece summary must have 7 parts: VEHICLE | SERIES | CENTER | OUTER | INNER | BOLTS | CAPS")
    if is_ecl and len(summary_parts) < 7:
        raise ValueError("ECL summary must have 7 parts: VEHICLE | SERIES | CENTER | OUTER | INNER | BOLTS | CAPS")

    vehicle = summary_parts[0].strip()
    wheel_series = summary_parts[1].strip()
    center_finish = summary_parts[2].strip()
    caps_finish = summary_parts[6].strip() if len(summary_parts) > 6 else summary_parts[3].strip()

    fitment_parts = fitment.split()
    if "/" not in fitment_parts[1]:
        raise ValueError("Fitment must include bolt pattern, slash, and centerbore")

    bolt_pattern = fitment_parts[0].strip()
    centerbore = fitment_parts[2].strip()
    output_lines = []

    if is_monoblock:
        wheel_specs = fitment_parts[3:]
        i = 0
        while i < len(wheel_specs):
            size = wheel_specs[i].upper()  # e.g., 24X9
            offset = wheel_specs[i + 1].upper().replace("ET", "").strip()

            diameter = size[:2]
            width = size[3:]
            model_name = wheel_series.upper().split("-M")[-1].strip()

            center_line = f'{diameter}X{width}.0M {model_name} / {bolt_pattern.upper()} / {centerbore} **{center_finish.upper()}**'
            if "XL CAPS" in caps_finish.upper():
                center_line += " MACHINE FOR XL CAPS"

            output_lines.append(center_line)
            output_lines.append(f'{size} +{offset}ET')
            output_lines.append("")  # spacer between front/rear
            i += 2

        output_lines.append(f'CAPS **{caps_finish.upper()}**')

    elif is_ecl:
        outer_finish = summary_parts[3].strip()
        inner_finish = summary_parts[4].strip()
        bolts_finish = summary_parts[5].strip()
        caps_line = f'CAPS **{caps_finish.upper()}**'

        i = 3
        while i < len(fitment_parts):
            if i + 6 > len(fitment_parts):
                raise ValueError("Incomplete ECL fitment block")

            center_forging = fitment_parts[i]
            ecl_keyword = fitment_parts[i + 1].lower()

            if ecl_keyword != "ecl":
                raise ValueError("Expected 'ecl' after center forging")

            diameter, center_width = center_forging.lower().split("x")
            center_width = float(center_width)
            i += 2

            size = fitment_parts[i]
            outer = fitment_parts[i + 1]
            inner = fitment_parts[i + 2]
            x_part = fitment_parts[i + 3]
            et_part = fitment_parts[i + 4]

            outer_val = float(outer.lower().replace("o", "").replace('"', ""))
            inner_val = float(inner.lower().replace("i", "").replace('"', ""))
            pad_height = x_part.split("=")[1]
            offset = et_part.upper().replace("ET", "").strip()

            output_lines.append(f'{diameter}" {outer_val}" OUTER 40H **{outer_finish.upper()}**')
            output_lines.append(f'{diameter}" {inner_val}" INNER 40H **{inner_finish.upper()}**')

            cut_spoke = " CUT SPOKE" if outer_val > center_width else ""
            model_name = wheel_series.upper().split("ECL", 1)[-1].strip()

            center_line = f'{diameter}x{int(center_width)}-ECL{cut_spoke} {model_name} X={pad_height} / {bolt_pattern.upper()} / {centerbore} **{center_finish.upper()}**'
            if "XL CAPS" in caps_finish.upper():
                center_line += " MACHINE FOR XL CAPS"

            output_lines.append(center_line)
            output_lines.append(f'{size.upper()} +{offset}ET')
            output_lines.append("")
            i += 5

        if "NO BOLTS" in bolts_finish.upper() or "BLIND BOLTS" in bolts_finish.upper():
            bolts_line = "NO BOLTS"
        else:
            bolts_color = bolts_finish.replace("BOLTS", "").strip()
            bolts_line = f'YES BOLTS **{bolts_color.upper()}**'

        output_lines.append(bolts_line)
        output_lines.append(caps_line)

    else:
        outer_finish = summary_parts[3].strip()
        inner_finish = summary_parts[4].strip()
        bolts_finish = summary_parts[5].strip()

        wheel_specs = fitment_parts[3:]
        i = 0
        while i < len(wheel_specs):
            size = wheel_specs[i]
            outer = wheel_specs[i + 1]
            inner = wheel_specs[i + 2]
            x_part = wheel_specs[i + 3]
            et_part = wheel_specs[i + 4]

            width = size[3:]
            diameter = size[:2]

            outer_val = outer.upper().replace("O", "")
            inner_val = inner.upper().replace("I", "")
            pad_height = x_part.split("=")[1]
            offset = et_part.upper().replace("ET", "").strip()

            outer_line = f'{diameter}" {outer_val} OUTER 40H **{outer_finish.upper()}**'
            inner_line = f'{diameter}" {inner_val} INNER 40H **{inner_finish.upper()}**'
            xl_caps_suffix = " MACHINE FOR XL CAPS" if "XL CAPS" in caps_finish.upper() else ""
            center_line = f'{wheel_series.upper()} X={pad_height} / {bolt_pattern.upper()} / {centerbore} **{center_finish.upper()}**{xl_caps_suffix}'
            size_line = f'{size.upper()} {offset}ET'

            output_lines.append(outer_line)
            output_lines.append(inner_line)
            output_lines.append(center_line)
            output_lines.append(size_line)
            output_lines.append("")
            i += 5

        if "NO BOLTS" in bolts_finish.upper() or "BLIND BOLTS" in bolts_finish.upper():
            bolts_line = "NO BOLTS"
        else:
            bolts_color = bolts_finish.replace("BOLTS", "").strip()
            bolts_line = f'YES BOLTS **{bolts_color.upper()}**'
        output_lines.append(bolts_line)
        output_lines.append(f'CAPS **{caps_finish.upper()}**')

    return "\n".join(output_lines)
