# This file is a part of FileStreamBot

import jinja2
import aiohttp
import aiofiles
import urllib.parse
from WebStreamer.vars import Var
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

async def render_page(db_id):
    file_data=await db.get_file(db_id)
    src = urllib.parse.urljoin(Var.URL, f'dl/{file_data["_id"]}')
    template_file="WebStreamer/template/req.html"
    file_size = humanbytes(int(u.headers.get('Content-Length')))
    tag = (file_data['mime_type']).split('/')[0].strip()

    if str((file_data['mime_type']).split('/')[0].strip()) == 'video':
            heading = 'Watch {}'.format(file_data['file_name'])
    elif str((file_data['mime_type']).split('/')[0].strip()) == 'audio':
            heading = 'Listen {}'.format(file_data['file_name'])
    else:
        template_file="WebStreamer/template/dl.html"
        heading = 'Download {}'.format(file_data['file_name'])

    with open(template_file) as f: 
        template = jinja2.Template(f.read()) 
        return template.render( 
            file_name=file_data['file_name'], 
            file_url=src, 
            file_size=file_size, 
            file_unique_id=file_data['unique_id'], 
            heading=heading,
            tag=tag
        )
