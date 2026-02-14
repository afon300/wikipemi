import http.server
import socketserver
import os
import argparse
import sys

def run_viewer(directory, port):
    """
    Starts a local web server to browse the scraped Wikipedia pages.
    """
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist. Run the scraper first.")
        sys.exit(1)

    os.chdir(directory)
    
    class UTF8Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Force the browser to interpret content as UTF-8
            if self.path.endswith(".html") or self.path == "/":
                self.send_header("Content-Type", "text/html; charset=utf-8")
            super().end_headers()
    
    Handler = UTF8Handler
    
    # Create a basic index.html if it doesn't exist to list pages nicely
    if not os.path.exists("index.html"):
        files = [f for f in os.listdir('.') if f.endswith('.html')]
        with open("index.html", "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>WikiPemi Archive Viewer</title>")
            f.write("<style>body{font-family:sans-serif; padding:40px; line-height:1.6;} a{color:#0645ad; text-decoration:none;} a:hover{text-decoration:underline;}</style>")
            f.write("</head><body>")
            f.write("<h1>📚 WikiPemi Local Archive</h1>")
            f.write(f"<p>Currently viewing <b>{len(files)}</b> pages.</p><ul>")
            for file in sorted(files):
                if file != "index.html":
                    name = file.replace(".html", "").replace("_", " ")
                    f.write(f"<li><a href='{file}'>{name}</a></li>")
            f.write("</ul></body></html>")

    print(f"\n🚀 WikiPemi Viewer started at: http://localhost:{port}")
    print(f"📁 Serving files from: {os.path.abspath('.')}")
    print("Press Ctrl+C to stop the server.\n")

    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down viewer...")
            httpd.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WikiPemi Local Archive Viewer")
    parser.add_argument("--dir", type=str, default="wiki_output", help="Directory to serve")
    parser.add_argument("--port", type=int, default=8000, help="Port to run on (default 8000)")
    
    args = parser.parse_args()
    run_viewer(args.dir, args.port)
