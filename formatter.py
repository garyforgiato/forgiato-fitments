def format_wheel_order(fitment, summary):
    summary_parts = summary.split("|")
    if len(summary_parts) < 7:
        raise ValueError("Summary must have 7 parts separated by |")

    vehicle = summary_parts[0].strip()
    wheel_series = summary_parts[1].strip()
    center_finish = summary_parts[2].strip()
    outer_finish = summary_parts[3].strip()
    inner_finish = summary_parts[4].strip()
    bolts_finish = summary_parts[5].strip()
    caps_finish = summary_parts[6].strip()

    fitment_parts = fitment.split()
    bolt_pattern = fitment_parts[0]
    centerbore = fitment_parts[2]
    wheel_specs = fitment_parts[3:]

    output_lines = []

    i = 0
    while i < len(wheel_specs):
        size = wheel_specs[i]
        outer = wheel_specs[i+1]
        inner = wheel_specs[i+2]
        x_part = wheel_specs[i+3]
        et_part = wheel_specs[i+4]

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

        i += 5

    if "NO BOLTS" in bolts_finish.upper() or "BLIND BOLTS" in bolts_finish.upper():
        bolts_line = "NO BOLTS"
    else:
        bolts_color = bolts_finish.replace("BOLTS", "").strip()
        bolts_line = f'YES BOLTS **{bolts_color.upper()}**'
    output_lines.append(bolts_line)

    caps_line = f'CAPS **{caps_finish.upper()}**'
    output_lines.append(caps_line)

    return "\n".join(output_lines)
