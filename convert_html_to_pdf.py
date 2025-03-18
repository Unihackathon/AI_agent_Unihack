
from playwright.async_api import async_playwright

async def convert_html_to_pdf(html_content, output_pdf):
    """
    Convert entire HTML document to PDF
    
    Args:
        html_content (str): The complete HTML content
        output_pdf (str): Path and name of the output PDF file
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Set the complete HTML content
        await page.set_content(html_content)
        
        # Wait for all scripts to load and Plotly to render
        await page.wait_for_timeout(3000)
        
        # Get the full height of the content
        content_height = await page.evaluate('document.body.scrollHeight')
        
        # Set viewport to capture full content
        await page.set_viewport_size({
            "width": 800,
            "height": content_height
        })
        
        # Generate PDF
        await page.pdf(
            path=output_pdf,
            format='A4',
            print_background=True,
            margin={'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'},
            prefer_css_page_size=False,
            width='800px',
            height=f'{content_height}px'
        )
        
        await browser.close()
