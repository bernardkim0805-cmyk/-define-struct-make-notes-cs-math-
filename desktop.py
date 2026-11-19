import webview

html = """<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
</head>
<body>
    <h1>MathCSNotes</h1>
    <p>Welcome to MathCSNotes! This is a simple note-taking application for math and computer science notes.</p>
    <div id="mathlatex"></div>
    <script>
     katex.render ("\\\\sum_{i=1}^n i = \\\\frac{n(n+1)}{2}", document.getElementById("mathlatex"));
    </script>
</body>
</html>
"""

webview.create_window("Math/CS Notes", html=html)
webview.start()
