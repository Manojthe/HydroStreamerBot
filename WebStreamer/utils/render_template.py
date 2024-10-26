import jinja2
import aiohttp
import aiofiles
import urllib.parse
from WebStreamer.vars import Var
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

async def render_page(db_id):
    file_data = await db.get_file(db_id)
    src = urllib.parse.urljoin(Var.URL, f'dl/{file_data["_id"]}')
    template_file = "WebStreamer/template/req.html"
    
    # Define tag based on mime type
    tag = (file_data['mime_type']).split('/')[0].strip()

    # Fetch file size using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(src) as u:
            if u.status == 200:
                file_size = humanbytes(int(u.headers.get('Content-Length', 0)))
            else:
                file_size = "Unknown"  # If fetching the file size fails

    # Set the heading based on file type
    if tag == 'video':
        heading = 'Watch {}'.format(file_data['file_name'])
    elif tag == 'audio':
        heading = 'Listen {}'.format(file_data['file_name'])
    else:
        template_file = "WebStreamer/template/dl.html"
        heading = 'Download {}'.format(file_data['file_name'])

    


    # Render the template with Jinja2
    with open(template_file) as f: 
        template = jinja2.Template(f.read()) 
        return template.render( 
            file_name=file_data['file_name'], 
            file_url=src, 
            file_size=file_size, 
            file_unique_id=file_data['file_unique_id'],  # Fixed from file_data['unique_id'] to file_data['file_unique_id']
            heading=heading,
            tag=tag
        )
