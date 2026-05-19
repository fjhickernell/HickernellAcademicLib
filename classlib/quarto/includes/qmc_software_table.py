import html
import yaml
from pathlib import Path


def render_qmc_software_table(data_path, mode="web"):
    data_path = Path(data_path)

    with data_path.open() as f:
        data = yaml.safe_load(f)

    data = sorted(data, key=lambda x: (x.get("name") or "").lower())

    show_description = mode == "web"
    show_contact = mode == "web"

    print("""
<table class="qmc-software-table">
<thead>
<tr>
    <th style="width: 40%;">Name</th>
    <th style="width: 16%;">Language</th>
    <th style="width: 22%;">Development Status</th>
""")

    if show_contact:
        print('  <th style="width: 22%;">Contact</th>')

    print("""
</tr>
</thead>
<tbody>
""")

    for row in data:
        name = html.escape(row.get("name", ""))
        url = row.get("url", "")
        language = html.escape(row.get("language", ""))
        status = row.get("status", "")
        raw_status = row.get("status", "")

        if mode == "web":
            status = raw_status.replace(
                ", Collaboration welcome",
                "<br>Collaboration welcome",
            )
        else:
            status = raw_status
        desc = html.escape(row.get("description", ""))

        if url:
            name_html = f'<a href="{html.escape(url)}">{name}</a>'
        else:
            name_html = name

        related = row.get("related", [])

        if related:
            related_links = []

            for r in related:
                rname = html.escape(r.get("name", ""))
                rurl = r.get("url", "")

                if rurl:
                    related_links.append(
                        f'<a href="{html.escape(rurl)}">{rname}</a>'
                    )
                else:
                    related_links.append(rname)

            related_html = ", ".join(related_links)

            if mode == "web":
                name_html += (
                    f'<br><span class="software-related">'
                    f'Related: {related_html}'
                    f'</span>'
                )
            else:
                name_html += (
                    f' <span class="software-related">'
                    f'(also {related_html})'
                    f'</span>'
                )

        if show_description and desc:
            name_html += (
                f'<br><span class="software-desc">{desc}</span>'
            )

        row_html = f"""
<tr>
  <td>{name_html}</td>
  <td>{language}</td>
  <td><span class="status-nowrap">{status}</span></td>
"""

        if show_contact:
            contacts = row.get("contact", [])
            contact_items = []

            for c in contacts:
                if isinstance(c, dict):
                    cname = html.escape(c.get("name", ""))
                    curl = c.get("url", "")

                    if curl:
                        label = (
                            f"✉ {cname}"
                            if curl.startswith("mailto:")
                            else cname
                        )

                        contact_items.append(
                            f'<a href="{html.escape(curl)}">{label}</a>'
                        )
                    else:
                        contact_items.append(cname)

                else:
                    contact_items.append(html.escape(str(c)))

            contact_str = "<br>".join(contact_items)

            row_html += f"  <td>{contact_str}</td>\n"

        row_html += "</tr>"

        print(row_html)

    print("""
</tbody>
</table>
""")