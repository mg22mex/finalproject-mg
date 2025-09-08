# Autosell.mx Frontend

React-based frontend for the Autosell.mx vehicle management system.

## Features

- 🚗 **Vehicle Management Dashboard** - Overview of all vehicles with statistics
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔍 **Advanced Search & Filtering** - Find vehicles quickly
- 📊 **Grid & List Views** - Choose your preferred display mode
- 🎨 **Modern UI** - Built with Tailwind CSS and Lucide React icons
- ⚡ **Real-time Updates** - React Query for data fetching and caching

## Tech Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Query** - Data fetching and state management
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm 9+

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navbar.tsx      # Main navigation
│   ├── VehicleCard.tsx # Vehicle display card
│   ├── VehicleTable.tsx # Vehicle list table
│   └── ...
├── pages/              # Page components
│   ├── Dashboard.tsx   # Main dashboard
│   ├── Vehicles.tsx    # Vehicle management
│   ├── Photos.tsx      # Photo management
│   └── Settings.tsx    # System settings
├── services/           # API services
│   └── api.ts         # Backend communication
├── types/              # TypeScript type definitions
│   └── vehicle.ts     # Vehicle-related types
├── App.tsx             # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## Development

### Adding New Components

1. Create component file in `src/components/`
2. Export as default
3. Import and use in pages

### Adding New Pages

1. Create page file in `src/pages/`
2. Add route in `App.tsx`
3. Add navigation link in `Navbar.tsx`

### API Integration

- Use functions from `src/services/api.ts`
- Use React Query for data fetching
- Handle loading and error states

## Styling

- **Tailwind CSS** for utility classes
- **Custom CSS** in `src/App.css` for complex styles
- **Component-specific styles** using Tailwind classes
- **Responsive design** with mobile-first approach

## State Management

- **React Query** for server state
- **React hooks** for local state
- **Context API** for global state (if needed)

## Performance

- **Code splitting** with React Router
- **Lazy loading** for components
- **Optimized images** and assets
- **Efficient re-renders** with React best practices

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow TypeScript best practices
2. Use functional components with hooks
3. Write clean, readable code
4. Test components thoroughly
5. Follow the existing code style

## License

MIT License - see main project README for details
