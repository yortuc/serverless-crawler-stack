from datetime import date


def render_html(listings):
    today = date.today().strftime("%B %d, %Y")

    str_listings = []
    for listing in listings:
        rend = f"""
            <div>
                <a href="{listing['link']}" target="_blank">[{listing['rent']}] - {listing['address']}</a>
            </div>
        """
        str_listings.append(rend)
    rend_listings = "".join(str_listings)

    html_output = f"""
        <html>
            <head><title>Evler</title></head>
            <body>
                <h3>Tarama Tarihi: {today}</h3>
                {rend_listings}
            </body>
        </html>
    """

    return html_output