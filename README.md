# Campus Navigation System

A mobile-friendly web application for campus navigation with QR code access, step-by-step directions, and multi-floor pathfinding.

## Features

- 🗺️ **Multi-Floor Navigation**: Navigate between Ground, First, Second, and Third floors
- 📱 **Mobile-Responsive**: Optimized for smartphones and tablets
- 🔍 **Smart Search**: Autocomplete suggestions for locations
- 📍 **Step-by-Step Directions**: Clear, detailed navigation instructions
- 🎨 **Dark Theme**: Professional dark mode interface
- 🔊 **Voice Navigation**: Text-to-speech for accessibility
- 📤 **Share Functionality**: Share directions with others

## Campus Layout

### Ground Floor - Main Block
**From Entrance:**
- **Right Side**: Administration Office → Dean/Principal Office → Library
- **Left Side**: Office Room → Cash Counter → Admission Cell → Dept. of Mechanical Engineering → Chairman Room → Steps
- **Near Steps**: Ladies Restroom → Drinking Water
- **Forward from Drinking Water**:
  - Left: Mini Auditorium
  - Middle: Electrical Machines Lab
  - Right: Tamil Mandram → Ramanujan Club → Shakespeare English Club → Health Centre → Chemistry Lab → Physics Lab

### First Floor
- **Centre**: Department of Computer Science and Engineering
- **Left Side of CSE**: LH5 → LH6 → LH7 → LH8
- **Right Side of CSE**: LH1 → LH2 → LH3 → LH4
- **Near Steps**: Boys Restroom → Drinking Water
- **From Drinking Water**:
  - Left: Counselling Room → Language Room
  - Middle: Electronics and Communication Lab
  - Right: Common Boys Room → ECE Lab

### Second Floor
- **Centre**: Department of Science and Humanities
- **Left Side**: LH13 → LH14 → LH15 → LH16
- **Right Side**: LH9 → LH10 → LH11 → LH12
- **Near Steps**: Boys Restroom (left), Ladies Restroom (right) → Drinking Water
- **From Drinking Water**: Common Girls Room → Digital and Electronic Systems Lab → Embedded Lab → Dept. of ECE → Circuits & Devices Lab → Optical & Microwave Lab

### Third Floor
- **Centre**: Centralised Lab
- **Left Side**: Torvalds Tech Lab → Power Unit → Placement Office → GD Room-1 → Panel Room → Waiting Room
- **Right Side**: Turning Minds Lab → Lanier Virtual Lab → Kernel Lab → Von Neumann Computing Lab → Charles Babbage → Power Unit

## Quick Start

1. **Access the Application**:
   - Open the web application in your browser
   - Or scan the QR code for quick mobile access

2. **Navigate**:
   - Enter your starting location (e.g., "Chairman Room")
   - Enter your destination (e.g., "LH1")
   - Click "Get Directions"

3. **Follow Directions**:
   - View step-by-step instructions
   - Use voice navigation for hands-free guidance
   - Share directions with others if needed

## Example Usage

**Sample Input:**
- Starting Point: `chairman room`
- Destination: `LH1`

**Expected Output:**
```
From Chairman Room
→ Take stairs and go up to First Floor
→ In the centre, you will witness the Department of Computer Science and Engineering
→ LH1 is next to the CSE Department
→ You have reached your destination: LH1!
```

## Technical Details

### Architecture
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5 (Dark Theme)
- **QR Code**: JavaScript QR code generator
- **Pathfinding**: Breadth-First Search (BFS) algorithm

### Key Files
- `app.py` - Main Flask application
- `navigation.py` - Navigation logic and pathfinding
- `campus_data.json` - Campus layout and location data
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and images

### API Endpoints
- `GET /` - Main navigation page
- `POST /navigate` - Get directions between locations
- `GET /api/locations` - Get all campus locations
- `GET /api/search` - Search locations by query

## Features in Detail

### QR Code Access
- Automatically generates QR code for the application URL
- Mobile-optimized scanning experience
- Instant access for visitors and new students

### Smart Location Search
- Real-time autocomplete suggestions
- Fuzzy matching for location names
- Floor-wise organization of results

### Multi-Floor Navigation
- Intelligent pathfinding across floors
- Clear stair transition instructions
- Optimized routes between any two locations

### Accessibility
- Voice navigation with text-to-speech
- High contrast mode support
- Touch-friendly interface
- Keyboard navigation support

## Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari (mobile)
- All modern mobile browsers

## Mobile Optimization

- Responsive design for all screen sizes
- Touch-friendly buttons and inputs
- Optimized QR code size for mobile scanning
- Fast loading with minimal data usage

## Deployment

### Local Development
```bash
python main.py
```

### Production
- Ready for deployment on Replit
- Can be exported for other hosting platforms
- Includes all necessary dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions about the campus navigation system, please contact the development team or create an issue in the repository.

---

**Campus Navigation System** - Making campus navigation simple and accessible for everyone.