# Map Integration in Story Engines

Guide for integrating JSON maps into Ink, Twine/SugarCube, and Generic (HTML/Markdown) outputs.

## Overview

Maps are integrated differently based on output format:

| Engine | Display | Availability | Format |
|--------|---------|--------------|--------|
| **Twine/SugarCube** | Embedded in HTML + separate "Maps" menu | Always (sidebar/menu) | PNG (embedded), SVG (referenced) |
| **Ink** | HTML wrapper with map sidebar gallery | Always (left sidebar) | PNG + SVG (in wrapper) |
| **Generic** | Linked map pages within story navigation | Always (navigation/links) | PNG + SVG (separate pages) |

## Twine/SugarCube Integration

### 1. StoryData Configuration

Add map metadata to StoryData JSON:

```twee
:: StoryData
{
  "ifid": "YOUR-IFID-HERE",
  "name": "Your Story Title",
  "sidebar": true,
  "maps": [
    {"id": "map-1", "name": "Goblin Hideout", "type": "battle", "session": 3},
    {"id": "map-2", "name": "Kingdom Overview", "type": "regional", "session": 1}
  ]
}
```

### 2. Map Gallery Passage

Create a "Maps" menu passage:

```twee
:: Maps [menu]
<div class="map-gallery">
  <h1>Maps</h1>
  
  <h2>Battle Maps</h2>
  <<for _map range $maps.filter(m => m.type === "battle")>>
    <<link _map.name "MapDisplay: " + _map.id>>
      <<set $currentMap = _map>>
    <</link>>
  <</for>>
  
  <h2>Regional Maps</h2>
  <<for _map range $maps.filter(m => m.type === "regional")>>
    <<link _map.name "MapDisplay: " + _map.id>>
      <<set $currentMap = _map>>
    <</link>>
  <</for>>
</div>
```

### 3. Map Display Passage

Display individual maps:

```twee
:: MapDisplay: map-1
<div class="map-container">
  [img[handouts/goblin-hideout.png]]
  
  <h2><<print $currentMap.name>></h2>
  
  <div class="map-info">
    <p><strong>Type:</strong> <<print $currentMap.type>></p>
    <p><strong>Session:</strong> <<print $currentMap.session>></p>
    
    <<if visited("Location: Goblin Hideout")>>
      <p><strong>Status:</strong> Visited</p>
    <</if>>
  </div>
  
  <<link "Back to Maps" "Maps">><</link>>
  <<link "Continue Story">>
    <<return>>
  <</link>>
</div>
```

### 4. Embed Battle Maps in Story Passages

When player enters battle location, display map:

```twee
:: Location: Goblin Hideout
You turn the corner and spot a goblin encampment hidden in the rocks!

[img[handouts/goblin-hideout.png]]

<<if $difficulty === "normal">>
  You see approximately 3-4 goblins, including a larger one wearing a chieftain's cloak.
<<elseif $difficulty === "hard">>
  You count 5-6 goblins, with several archers positioned on the higher rocks.
<</if>>

<<link "Prepare for Battle" "Battle: Goblin Camp">><</link>>
<<link "Try to Hide" "Scout Goblin Camp">><</link>>
<<link "Retreat" "Previous Location">><</link>>
```

### 5. CSS Styling (Optional)

```css
.map-gallery {
  padding: 1em;
  border: 1px solid #ccc;
}

.map-gallery h2 {
  margin-top: 1em;
  font-size: 1.2em;
}

.map-container {
  max-width: 100%;
  padding: 1em;
}

.map-container img {
  max-width: 100%;
  border: 2px solid #333;
  margin: 1em 0;
}

.map-info {
  background: #f0f0f0;
  padding: 0.5em;
  margin: 1em 0;
  border-left: 4px solid #0066cc;
}
```

## Ink Integration

### 1. Map Metadata in Compiled JSON

When compiling Ink, add map metadata to story.json:

```json
{
  "maps": [
    {
      "id": "map-1",
      "name": "Goblin Hideout",
      "type": "battle",
      "session": 3,
      "image": "handouts/goblin-hideout.png",
      "reference": "reference/goblin-hideout.svg",
      "encounters": ["goblin-scout", "chief-grok"]
    },
    {
      "id": "map-2",
      "name": "Kingdom Overview",
      "type": "regional",
      "session": 1,
      "image": "handouts/kingdom-overview.png",
      "reference": "reference/kingdom-overview.svg"
    }
  ],
  "story": { /* compiled ink JSON */ }
}
```

### 2. HTML Wrapper with Map Sidebar

Create an enhanced HTML wrapper (`story.html`) with sidebar gallery:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Story with Maps</title>
  <style>
    body { font-family: Georgia, serif; margin: 0; display: flex; }
    
    #sidebar {
      width: 250px;
      background: #f5f5f5;
      border-right: 1px solid #ccc;
      overflow-y: auto;
      padding: 1em;
    }
    
    #sidebar h2 { font-size: 1.1em; margin-top: 0; }
    
    #sidebar .map-item {
      padding: 0.5em;
      cursor: pointer;
      border: 1px solid #ddd;
      margin: 0.5em 0;
      border-radius: 3px;
    }
    
    #sidebar .map-item:hover { background: #eee; }
    #sidebar .map-item.active { background: #0066cc; color: white; }
    
    #story-container { flex: 1; padding: 2em; line-height: 1.6; }
    
    .map-display {
      max-width: 100%;
      margin: 2em 0;
      padding: 1em;
      background: #f9f9f9;
      border: 1px solid #ddd;
    }
    
    .map-display img { max-width: 100%; height: auto; }
    .map-display h3 { margin-top: 0; }
    .map-info { font-size: 0.9em; color: #666; }
  </style>
</head>
<body>
  <div id="sidebar">
    <h2>Maps</h2>
    <div id="map-gallery"></div>
  </div>
  
  <div id="story-container">
    <div id="story"></div>
  </div>
  
  <!-- Ink runtime -->
  <script src="ink.js"></script>
  <script>
    // Load story with maps
    fetch('story.json')
      .then(r => r.json())
      .then(data => {
        window.story = new inkjs.Story(data.story);
        window.maps = data.maps;
        
        // Build map gallery
        const gallery = document.getElementById('map-gallery');
        data.maps.forEach(map => {
          const item = document.createElement('div');
          item.className = 'map-item';
          item.textContent = map.name;
          item.onclick = () => displayMap(map);
          gallery.appendChild(item);
        });
      });
    
    function displayMap(map) {
      const container = document.getElementById('story-container');
      container.innerHTML = `
        <div class="map-display">
          <h3>${map.name}</h3>
          <img src="${map.image}" alt="${map.name}">
          <div class="map-info">
            <p><strong>Type:</strong> ${map.type}</p>
            <p><strong>Session:</strong> ${map.session || 'N/A'}</p>
            <p><a href="${map.reference}" download>Download SVG (editable)</a></p>
          </div>
          <button onclick="continueStory()">Back to Story</button>
        </div>
      `;
    }
    
    function continueStory() {
      // Reload story display
      // Implementation depends on Ink runtime setup
    }
  </script>
</body>
</html>
```

### 3. Ink Script Integration

In your Ink story, reference maps by ID:

```ink
=== goblin_encounter ===
You turn the corner and spot a goblin encampment!

~displayMap("map-1")  // Trigger map display

* [Prepare for Battle] -> battle_start
* [Try to Hide] -> scout_camp
* [Retreat] -> run_away
```

JavaScript handler:
```javascript
function displayMap(mapId) {
  const map = window.maps.find(m => m.id === mapId);
  if (map) {
    displayMap(map);
  }
}
```

## Generic (Markdown → HTML) Integration

### 1. Maps Index Page

Create `output/generic/maps.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Map Index</title>
  <style>
    body { font-family: Georgia, serif; max-width: 900px; margin: 0 auto; padding: 2em; }
    .map-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5em; margin-top: 2em; }
    .map-card { border: 1px solid #ddd; padding: 1em; border-radius: 5px; cursor: pointer; transition: all 0.3s; }
    .map-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); transform: translateY(-2px); }
    .map-card img { width: 100%; height: 150px; object-fit: cover; margin-bottom: 1em; }
    .map-card h3 { margin: 0.5em 0; }
    .map-card p { font-size: 0.9em; color: #666; margin: 0.3em 0; }
    .filters { margin: 1em 0; }
    .filter-btn { padding: 0.5em 1em; margin: 0.3em; border: 1px solid #999; background: white; cursor: pointer; border-radius: 3px; }
    .filter-btn.active { background: #0066cc; color: white; border-color: #0066cc; }
  </style>
</head>
<body>
  <h1>Map Index</h1>
  
  <div class="filters">
    <button class="filter-btn active" onclick="filterMaps('all')">All Maps</button>
    <button class="filter-btn" onclick="filterMaps('battle')">Battle Maps</button>
    <button class="filter-btn" onclick="filterMaps('regional')">Regional Maps</button>
    <button class="filter-btn" onclick="filterMaps('location')">Location Maps</button>
  </div>
  
  <div class="map-grid" id="map-grid"></div>
  
  <script>
    const maps = [
      {"id": "map-1", "name": "Goblin Hideout", "type": "battle", "image": "handouts/goblin-hideout.png"},
      {"id": "map-2", "name": "Kingdom Overview", "type": "regional", "image": "handouts/kingdom-overview.png"}
      // ...load from maps.json or inline
    ];
    
    function renderMaps(filter = 'all') {
      const grid = document.getElementById('map-grid');
      grid.innerHTML = '';
      
      maps
        .filter(m => filter === 'all' || m.type === filter)
        .forEach(map => {
          const card = document.createElement('div');
          card.className = 'map-card';
          card.innerHTML = `
            <img src="${map.image}" alt="${map.name}">
            <h3>${map.name}</h3>
            <p><strong>Type:</strong> ${map.type}</p>
            <a href="maps/map-${map.id}.html">View Details →</a>
          `;
          grid.appendChild(card);
        });
    }
    
    function filterMaps(type) {
      // Update active button
      document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
      renderMaps(type);
    }
    
    renderMaps();
  </script>
</body>
</html>
```

### 2. Individual Map Page Template

Create `output/generic/maps/map-map-1.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Goblin Hideout - Map</title>
  <style>
    body { font-family: Georgia, serif; max-width: 1000px; margin: 0 auto; padding: 2em; }
    .breadcrumb { margin-bottom: 1em; }
    .breadcrumb a { margin: 0 0.5em; }
    .map-container img { max-width: 100%; border: 2px solid #333; margin: 1em 0; }
    .map-info { background: #f5f5f5; padding: 1em; margin: 1em 0; border-left: 4px solid #0066cc; }
    .details-table { width: 100%; border-collapse: collapse; }
    .details-table td { padding: 0.5em; border-bottom: 1px solid #ddd; }
    .details-table td:first-child { font-weight: bold; width: 150px; }
    .actions { margin: 2em 0; }
    .btn { padding: 0.7em 1.5em; margin: 0.3em; border: 1px solid #0066cc; background: white; color: #0066cc; cursor: pointer; border-radius: 3px; text-decoration: none; display: inline-block; }
    .btn.primary { background: #0066cc; color: white; }
  </style>
</head>
<body>
  <div class="breadcrumb">
    <a href="../">Story Home</a> / <a href="../maps.html">Maps</a> / Goblin Hideout
  </div>
  
  <h1>Goblin Hideout</h1>
  
  <div class="map-container">
    <img src="../handouts/goblin-hideout.png" alt="Goblin Hideout Battle Map">
  </div>
  
  <div class="map-info">
    <h2>Map Details</h2>
    <table class="details-table">
      <tr><td>Type</td><td>Battle Map</td></tr>
      <tr><td>Session</td><td>Session 3</td></tr>
      <tr><td>Grid Size</td><td>20×20 squares</td></tr>
      <tr><td>Scale</td><td>5 feet per square</td></tr>
      <tr><td>Encounters</td><td>Goblin Scout (CR 1/8), Chief Grok (CR 1/2)</td></tr>
    </table>
  </div>
  
  <div class="map-info">
    <h2>GM Notes</h2>
    <ul>
      <li><strong>Secret Door</strong> at position (8, 12) - requires DC 15 Perception check</li>
      <li><strong>Trap</strong> at position (10, 10) - DC 14 save for half damage (2d6)</li>
      <li>Light source: Campfire at (15, 15) - illuminates 30 feet</li>
      <li>Treasure: 50 gold and a potion of healing in chest at (5, 5)</li>
    </ul>
  </div>
  
  <div class="actions">
    <a href="../handouts/goblin-hideout.png" download class="btn">Download PNG</a>
    <a href="../reference/goblin-hideout.svg" download class="btn">Download SVG (Editable)</a>
    <a href="../maps.html" class="btn primary">Back to Maps</a>
  </div>
</body>
</html>
```

### 3. Link Maps from Story Pages

In your story HTML, add map references:

```html
<p>You approach the <a href="maps/map-map-1.html">Goblin Hideout</a>...</p>

<!-- Or use a "View Map" button -->
<button onclick="window.location.href='maps/map-map-1.html'">View Battle Map</button>
```

## Implementation Checklist

### For Each Engine:

- [ ] Export maps to PNG (handouts) and SVG (reference)
- [ ] Create map display files (passages, HTML pages, etc.)
- [ ] Add map metadata to story configuration
- [ ] Link maps from story content
- [ ] Create navigation/menu for map access
- [ ] Test map loading and display
- [ ] Verify PNG quality for printing
- [ ] Test SVG download and edit capability
- [ ] Add CSS styling for map presentation
- [ ] Document map metadata format

### Testing

1. **SugarCube**: Open story.html, navigate to "Maps" menu, click map links
2. **Ink**: Open story.html, click map sidebar items, verify sidebar gallery
3. **Generic**: Open maps.html, click individual map cards, verify details page

## Performance Notes

- **PNG Maps**: Embed directly in passages/wrapper (no external load)
- **SVG Maps**: Link/download only (too large to embed in story)
- **Large Maps**: Consider splitting into regions or tiles
- **Handouts**: Use PNG for player-facing (faster, no editing)
- **Reference**: Use SVG for GM use (editable, scalable)

## Accessibility

- [ ] All map images have alt text
- [ ] Map menu has keyboard navigation (tabindex)
- [ ] Color-blind friendly terrain colors (test with Colorblind Simulator)
- [ ] SVG maps include text descriptions
- [ ] Link text clearly indicates "Map" or "View Map"
- [ ] Adequate contrast ratio (WCAG AA 4.5:1)

---

Next: Run `speckit.compile` to automatically generate all map integration files for your output engine!
