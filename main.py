from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import random

app = FastAPI(title="Simple Joke Generator")

# HTML template embedded in Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Joke Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            background: white;
        }
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn-container {
            display: flex;
            gap: 15px;
            margin: 30px 0;
        }
        button {
            flex: 1;
            padding: 15px 25px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .btn-secondary {
            background: linear-gradient(135deg, #f093fb, #f5576c);
            color: white;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .joke-container {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-top: 25px;
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .joke-text {
            font-size: 1.2rem;
            line-height: 1.6;
            color: #333;
        }
        .setup {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
        }
        .delivery {
            color: #764ba2;
            font-style: italic;
        }
        .loading {
            color: #667eea;
            font-size: 1.1rem;
        }
        .error {
            background: #ffe6e6;
            color: #d63031;
            border: 1px solid #fab1a0;
        }
        .joke-meta {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
            font-size: 0.9rem;
            color: #666;
        }
        .meta-item {
            background: white;
            padding: 5px 12px;
            border-radius: 15px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Joke Generator</h1>
        
        <form id="jokeForm">
            <div class="form-group">
                <label for="category">Category:</label>
                <select id="category" name="category">
                    <option value="Any">Any</option>
                    <option value="Programming">Programming</option>
                    <option value="Miscellaneous">Miscellaneous</option>
                    <option value="Pun">Pun</option>
                    <option value="Spooky">Spooky</option>
                    <option value="Christmas">Christmas</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="joke_type">Joke Type:</label>
                <select id="joke_type" name="joke_type">
                    <option value="Any">Any</option>
                    <option value="single">Single (One-liner)</option>
                    <option value="twopart">Two Part (Setup & Delivery)</option>
                </select>
            </div>
            
            <div class="btn-container">
                <button type="submit" class="btn-primary">Get Joke!</button>
                <button type="button" class="btn-secondary" id="randomJoke">Surprise Me!</button>
            </div>
        </form>
        
        <div class="joke-container" id="jokeContainer">
            <div id="jokeContent">
                <div class="joke-text">
                    🎪 Ready to laugh? Click a button to fetch your first joke!
                </div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('jokeForm');
        const randomBtn = document.getElementById('randomJoke');
        const jokeContainer = document.getElementById('jokeContainer');
        const jokeContent = document.getElementById('jokeContent');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            await fetchJoke(`/api/joke?${params}`);
        });

        randomBtn.addEventListener('click', () => fetchJoke('/api/random-joke'));

        async function fetchJoke(url) {
            try {
                jokeContent.innerHTML = '<div class="loading">🔄 Fetching joke...</div>';
                jokeContainer.classList.remove('error');
                
                const response = await fetch(url);
                const data = await response.json();
                
                if (!response.ok) throw new Error(data.detail);
                
                displayJoke(data.joke);
            } catch (error) {
                jokeContainer.classList.add('error');
                jokeContent.innerHTML = `<div class="joke-text">❌ ${error.message}</div>`;
            }
        }

        function displayJoke(joke) {
            let html = '';
            
            if (joke.type === 'twopart') {
                html = `
                    <div class="joke-text">
                        <div class="setup">${joke.setup}</div>
                        <div class="delivery">${joke.delivery}</div>
                    </div>
                `;
            } else {
                html = `<div class="joke-text">${joke.joke}</div>`;
            }
            
            html += `
                <div class="joke-meta">
                    <div class="meta-item">📂 ${joke.category}</div>
                    <div class="meta-item">💬 ${joke.type}</div>
                    <div class="meta-item">#${joke.id}</div>
                </div>
            `;
            
            jokeContent.innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main page"""
    return HTML_TEMPLATE

@app.get("/api/joke")
async def get_joke(category: str = "Any", joke_type: str = "Any"):
    """Fetch a joke from JokeAPI"""
    try:
        url = f"https://v2.jokeapi.dev/joke/{category}"
        params = {
            "blacklistFlags": "nsfw,religious,political,racist,sexist,explicit",
            "format": "json"
        }
        
        if joke_type != "Any":
            params["type"] = joke_type
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                joke_data = response.json()
                if joke_data.get("error"):
                    raise HTTPException(status_code=404, detail="No joke found")
                return {"success": True, "joke": joke_data}
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch joke")
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/random-joke")
async def get_random_joke():
    """Get a random joke with random parameters"""
    categories = ["Any", "Programming", "Miscellaneous", "Pun", "Spooky"]
    joke_types = ["Any", "single", "twopart"]
    
    return await get_joke(
        category=random.choice(categories),
        joke_type=random.choice(joke_types)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
