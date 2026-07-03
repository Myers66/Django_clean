from aiohttp import web

async def upload(request):
    total_size = 0
    async for chunk in request.content.iter_chunked(8192):
        total_size += len(chunk)
    return web.json_response({"size": total_size})

def main():
    app = web.Application()
    app.router.add_post('/api/upload/', upload)
    web.run_app(app, host='127.0.0.1', port=8080)

if __name__ == '__main__':
    main()