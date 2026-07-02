# SecureStego Frontend UI Documentation

This document provides comprehensive documentation for the frontend UI of the SecureStego project. It covers the architecture, folder structure, components, styling, and how to modify the design.

---

## 1. Frontend Overview

### Architecture
The frontend is built as a **Single Page Application (SPA)** using React with client-side routing. The application follows a component-based architecture where UI elements are broken down into reusable components.

### Framework & Technologies
- **React 18.3.1** - UI library for building the interface
- **React Router DOM 6.23.1** - Client-side routing
- **Tailwind CSS 3.4.3** - Utility-first CSS framework for styling
- **Framer Motion 11.2.10** - Animation library for smooth transitions
- **Lucide React 0.379.0** - Icon library
- **Vite 6.3.5** - Build tool and development server

### Organization
- **Pages** - Main route-level components (Landing, HideMessage, ExtractMessage, About, Contact)
- **Components** - Reusable UI components organized by type (ui, layout, common)
- **Services** - API and business logic services (encryption, steganography)
- **Hooks** - Custom React hooks for state management
- **Utils** - Utility functions for crypto and API operations
- **Assets** - Static assets (currently empty, icons are from Lucide)

---

## 2. Project Folder Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/           # Shared utility components
│   │   │   └── SectionHeader.jsx
│   │   ├── layout/           # Layout components (Navbar, Footer)
│   │   │   ├── Footer.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── TwoColumnLayout.jsx
│   │   └── ui/               # Reusable UI components
│   │       ├── ActionCard.jsx
│   │       ├── Button.jsx
│   │       ├── Card.jsx
│   │       ├── DebugPanel.jsx
│   │       ├── FileUpload.jsx
│   │       ├── Input.jsx
│   │       ├── MessageCard.jsx
│   │       ├── PasswordCard.jsx
│   │       ├── PasswordInput.jsx
│   │       ├── SecurityInfoBar.jsx
│   │       ├── Textarea.jsx
│   │       └── UploadCard.jsx
│   ├── pages/                # Route-level page components
│   │   ├── About.jsx
│   │   ├── Contact.jsx
│   │   ├── ExtractMessage.jsx
│   │   ├── HideMessage.jsx
│   │   └── Landing.jsx
│   ├── hooks/                # Custom React hooks
│   │   ├── index.js
│   │   ├── useEncryption.js
│   │   └── useSteganography.js
│   ├── services/             # API and business logic services
│   │   ├── apiService.js
│   │   ├── encryptionService.js
│   │   └── index.js
│   ├── utils/                # Utility functions
│   │   ├── api.js
│   │   ├── crypto.js
│   │   └── index.js
│   ├── constants/            # Application constants
│   ├── context/              # React Context providers
│   ├── types/                # TypeScript type definitions
│   ├── assets/               # Static assets (images, fonts)
│   ├── App.jsx               # Main application component with routing
│   ├── main.jsx              # Application entry point
│   └── index.css             # Global CSS and Tailwind directives
├── index.html                # HTML template
├── package.json              # Dependencies and scripts
├── tailwind.config.js        # Tailwind CSS configuration
├── vite.config.js            # Vite build configuration
└── postcss.config.js         # PostCSS configuration
```

### Folder Purposes

| Folder | Purpose |
|--------|---------|
| `src/components/common` | Shared utility components used across multiple pages (e.g., SectionHeader) |
| `src/components/layout` | Layout components that structure the page (Navbar, Footer) |
| `src/components/ui` | Reusable UI building blocks (Card, Button, Input, etc.) |
| `src/pages` | Route-level components that represent full pages |
| `src/hooks` | Custom React hooks for reusable stateful logic |
| `src/services` | API calls and business logic (encryption, steganography) |
| `src/utils` | Pure utility functions (crypto operations, API helpers) |
| `src/constants` | Application-wide constants and configuration |
| `src/context` | React Context providers for global state |
| `src/types` | TypeScript type definitions (if using TypeScript) |
| `src/assets` | Static assets like images, logos, fonts |

---

## 3. Page Structure

### Landing.jsx
**Purpose:** Landing page with hero section, feature highlights, and call-to-action buttons.

**Route:** `/`

**Components Used:**
- Button (from `components/ui/Button`)

**Styles:** Global styles from `index.css`, Tailwind utility classes

**Services:** None (static content only)

---

### HideMessage.jsx
**Purpose:** Main page for hiding secret messages in images/videos. Handles file upload, message input, password entry, and encryption.

**Route:** `/hide`

**Components Used:**
- UploadCard (`components/ui/UploadCard`)
- MessageCard (`components/ui/MessageCard`)
- PasswordCard (`components/ui/PasswordCard`)
- ActionCard (`components/ui/ActionCard`)
- SecurityInfoBar (`components/ui/SecurityInfoBar`)

**Styles:** Global styles from `index.css`, Tailwind utility classes

**Services:**
- `encryptMessage` (from `services`)
- `embedMessage` (from `services`)
- `encryptionService` (from `services`)

**State:**
- `file` - Selected file for steganography
- `password` - Encryption password
- `message` - Secret message to hide
- `isProcessing` - Loading state
- `showSuccess` - Success state
- `error` - Error message
- `encryptionData` - Encrypted data
- `stegoData` - Steganography result

---

### ExtractMessage.jsx
**Purpose:** Page for extracting hidden messages from steganographic images/videos. Handles file upload, password entry, and decryption.

**Route:** `/extract`

**Components Used:**
- UploadCard (`components/ui/UploadCard`)
- PasswordCard (`components/ui/PasswordCard`)
- ActionCard (`components/ui/ActionCard`)
- Card (`components/ui/Card`) - for security note
- SecurityInfoBar (`components/ui/SecurityInfoBar`)

**Styles:** Global styles from `index.css`, Tailwind utility classes

**Services:**
- `decryptMessage` (from `services`)
- `extractMessage` (from `services`)
- `encryptionService` (from `services`)

**State:**
- `file` - Selected file for extraction
- `password` - Decryption password
- `isProcessing` - Loading state
- `extractedMessage` - Decrypted message
- `showResult` - Result display state
- `error` - Error message
- `decryptionData` - Decrypted data
- `stegoData` - Steganography data

---

### About.jsx
**Purpose:** Informational page describing the project, core technologies, and tech stack.

**Route:** `/about`

**Components Used:**
- Card (`components/ui/Card`)

**Styles:** Global styles from `index.css`, Tailwind utility classes

**Services:** None (static content only)

---

### Contact.jsx
**Purpose:** Contact page with contact information, social links, and a contact form.

**Route:** `/contact`

**Components Used:**
- Card (`components/ui/Card`)
- Button (`components/ui/Button`)
- Input (`components/ui/Input`)
- Textarea (`components/ui/Textarea`)

**Styles:** Global styles from `index.css`, Tailwind utility classes

**Services:** None (form is UI only)

---

## 4. Components Documentation

### Card
**Location:** `src/components/ui/Card.jsx`

**Purpose:** Base card component with glass morphism effect and animation. Used as a wrapper for all card-based UI elements.

**Props:**
- `children` (ReactNode) - Content to display inside the card
- `className` (string) - Additional Tailwind classes
- `...props` - Any other props passed to the motion.div

**State:** None (stateless component)

**Important Functions:** None

**Parent Components:** UploadCard, MessageCard, PasswordCard, ActionCard, About, Contact

**Child Components:** None (wrapper component)

**How it works:**
- Wraps children in a motion.div with fade-in animation
- Applies `glass-card-hover` class for glass morphism styling
- Uses `p-7` (28px padding) by default
- Supports additional className for customization

---

### Button
**Location:** `src/components/ui/Button.jsx`

**Purpose:** Reusable button component with multiple variants and hover animations.

**Props:**
- `children` (ReactNode) - Button content
- `variant` (string) - Button style: 'primary', 'secondary', 'outline', 'danger'
- `className` (string) - Additional Tailwind classes
- `...props` - Any standard button props (onClick, disabled, etc.)

**State:** None (stateless component)

**Important Functions:** None

**Parent Components:** ActionCard, Landing, Contact

**Child Components:** None

**How it works:**
- Uses Framer Motion for hover/tap animations (scale 1.02 on hover, 0.98 on tap)
- Primary variant: Gradient background (accent-primary to accent-secondary), white text, glow effect
- Secondary variant: Glass background, border, hover effect
- Outline variant: Transparent background, accent border
- Danger variant: Red tinted background and border

---

### UploadCard
**Location:** `src/components/ui/UploadCard.jsx`

**Purpose:** File upload card with drag-and-drop support for images and videos.

**Props:**
- `onFileSelect` (function) - Callback when file is selected
- `file` (File) - Currently selected file
- `onRemove` (function) - Callback to remove file
- `label` (string) - Optional label (currently unused)

**State:**
- `isDragging` (boolean) - Drag state for visual feedback

**Important Functions:**
- `handleDragOver` - Sets dragging state
- `handleDragLeave` - Clears dragging state
- `handleDrop` - Processes dropped file
- `handleFileChange` - Processes file input change
- `handleRemove` - Removes selected file

**Parent Components:** HideMessage, ExtractMessage

**Child Components:** Card, SectionHeader

**How it works:**
- Displays drag-and-drop zone when no file is selected
- Shows file preview with icon (Film for video, FileImage for image) when file is selected
- Supports both drag-and-drop and click-to-browse
- Validates file type (image/*, video/*)

---

### MessageCard
**Location:** `src/components/ui/MessageCard.jsx`

**Purpose:** Card for entering secret messages with character counter and capacity indicator.

**Props:**
- `message` (string) - Current message value
- `onChange` (function) - Change handler
- `placeholder` (string) - Placeholder text
- `maxLength` (number) - Maximum character limit (default: 10000)
- `showCapacity` (boolean) - Whether to show capacity text
- `capacityText` (string) - Capacity information text

**State:** None (controlled component)

**Important Functions:** None

**Parent Components:** HideMessage

**Child Components:** Card, SectionHeader, Textarea

**How it works:**
- Contains a textarea for message input
- Shows character counter (current / maxLength)
- Optionally shows capacity text (e.g., available KB for steganography)
- Uses flex layout to fill available height

---

### PasswordCard
**Location:** `src/components/ui/PasswordCard.jsx`

**Purpose:** Password input card with strength indicator and validation rules.

**Props:**
- `password` (string) - Current password value
- `onChange` (function) - Change handler
- `placeholder` (string) - Placeholder text
- `showStrength` (boolean) - Whether to show strength indicator
- `strength` (object) - Strength object with score and label

**State:** None (controlled component)

**Important Functions:**
- `getValidationStatus` - Returns validation status for each rule (valid/invalid/pending)

**Parent Components:** HideMessage, ExtractMessage

**Child Components:** Card, SectionHeader, PasswordInput

**How it works:**
- Contains password input with show/hide toggle
- Optionally displays strength indicator with 4-bar visualization
- Shows validation rules (8+ chars, uppercase, lowercase, number)
- Each rule shows checkmark when valid, X when invalid

---

### ActionCard
**Location:** `src/components/ui/ActionCard.jsx`

**Purpose:** Action card with a large button for primary actions (encrypt/decrypt).

**Props:**
- `onClick` (function) - Click handler
- `disabled` (boolean) - Whether button is disabled
- `isProcessing` (boolean) - Whether action is in progress
- `buttonText` (string) - Button text when not processing
- `processingText` (string) - Button text when processing
- `icon` (LucideIcon) - Icon component to display
- `error` (string) - Error message to display

**State:** None (controlled component)

**Important Functions:** None

**Parent Components:** HideMessage, ExtractMessage

**Child Components:** Card, Button

**How it works:**
- Displays error message if present
- Contains a full-width button (68px height)
- Shows spinning icon and processing text when isProcessing is true
- Shows static icon and buttonText when not processing
- Button is disabled when disabled prop is true

---

### SecurityInfoBar
**Location:** `src/components/ui/SecurityInfoBar.jsx`

**Purpose:** Bottom feature bar displaying security features (AES-256-GCM, Argon2id, etc.).

**Props:** None

**State:** None (static component)

**Important Functions:** None

**Parent Components:** HideMessage, ExtractMessage

**Child Components:** None

**How it works:**
- Displays 5 security feature sections in a horizontal layout
- Each section has an icon, title, and subtitle
- Responsive: 5 columns on desktop, 1 column on mobile with dividers
- Uses glass-card styling

---

### Navbar
**Location:** `src/components/layout/Navbar.jsx`

**Purpose:** Fixed navigation bar with logo, navigation links, and mobile menu.

**Props:** None

**State:**
- `isOpen` (boolean) - Mobile menu open/close state

**Important Functions:**
- `isActive` - Checks if a route is currently active

**Parent Components:** App

**Child Components:** None

**How it works:**
- Fixed position at top with glass morphism effect
- Displays logo (Shield icon + "SecureStego" text)
- Desktop: Horizontal navigation links with active indicator
- Mobile: Hamburger menu that opens/closes with animation
- Uses Framer Motion for mobile menu animation
- Active route shows gradient underline indicator

---

### Footer
**Location:** `src/components/layout/Footer.jsx`

**Purpose:** Footer with brand info, quick links, and social icons.

**Props:** None

**State:** None (static component)

**Important Functions:** None

**Parent Components:** App

**Child Components:** None

**How it works:**
- 3-column layout: Brand, Quick Links, Connect
- Brand section: Logo + description
- Quick Links: Navigation links
- Connect: Social media icons (GitHub, Mail)
- Bottom bar: Copyright + "Made with Heart" message

---

### SectionHeader
**Location:** `src/components/common/SectionHeader.jsx`

**Purpose:** Reusable section header with icon and title for cards.

**Props:**
- `icon` (LucideIcon) - Icon component to display
- `title` (string) - Section title
- `className` (string) - Additional Tailwind classes

**State:** None (stateless component)

**Important Functions:** None

**Parent Components:** UploadCard, MessageCard, PasswordCard, ActionCard

**Child Components:** None

**How it works:**
- Displays icon in a rounded container with border
- Displays title as text-2xl (32px) font-semibold
- Uses flex layout with space between icon and title

---

### Input
**Location:** `src/components/ui/Input.jsx`

**Purpose:** Reusable text input component with optional label.

**Props:**
- `label` (string) - Input label
- `type` (string) - Input type (default: 'text')
- `className` (string) - Additional Tailwind classes
- `...props` - Any standard input props

**State:** None (controlled component)

**Parent Components:** Contact

**Child Components:** None

**How it works:**
- Wraps input with optional label
- Applies `input-field` utility class for styling
- Label uses text-text-secondary color

---

### Textarea
**Location:** `src/components/ui/Textarea.jsx`

**Purpose:** Reusable textarea component with optional label.

**Props:**
- `label` (string) - Textarea label
- `className` (string) - Additional Tailwind classes
- `...props` - Any standard textarea props

**State:** None (controlled component)

**Parent Components:** MessageCard, Contact

**Child Components:** None

**How it works:**
- Wraps textarea with optional label
- Applies `input-field` utility class for styling
- Label uses text-text-secondary color
- Textarea is resizable (resize-y)

---

### PasswordInput
**Location:** `src/components/ui/PasswordInput.jsx`

**Purpose:** Password input with show/hide toggle button.

**Props:**
- `label` (string) - Input label
- `className` (string) - Additional Tailwind classes
- `...props` - Any standard input props (value, onChange, etc.)

**State:**
- `showPassword` (boolean) - Toggle state for password visibility

**Important Functions:** None

**Parent Components:** PasswordCard

**Child Components:** None

**How it works:**
- Wraps input with optional label
- Adds eye icon button to toggle password visibility
- Shows Eye icon when password is hidden, EyeOff when visible
- Applies `input-field` utility class for styling

---

## 5. Styling Guide

### index.css
**Location:** `src/index.css`

**What it controls:**
- Global CSS variables and utility classes
- Tailwind CSS directives (@tailwind base, components, utilities)
- Custom utility classes for glass morphism, buttons, inputs, cards
- Custom scrollbar styling

**Which pages use it:** All pages (imported in main.jsx)

**Which components depend on it:** All components (via Tailwind classes)

**Where to edit:**

#### Colors
Edit in `tailwind.config.js`:
```javascript
colors: {
  bg: { primary: '#070B12', secondary: '#0E131B' },
  card: { primary: '#0F172A', secondary: '#1B2234' },
  accent: { primary: '#00E5C2', secondary: '#00BFA5' },
  text: { primary: '#F5F7FA', secondary: '#94A3B8', muted: '#6D7788' },
  border: { primary: 'rgba(0, 245, 195, 0.12)' }
}
```

#### Buttons
Edit in `index.css` (`.btn-primary` class) and `src/components/ui/Button.jsx`:
```css
.btn-primary {
  @apply bg-gradient-to-r from-accent-primary to-accent-secondary text-white ...;
}
```

#### Cards
Edit in `index.css` (`.glass-card`, `.glass-card-hover` classes) and `src/components/ui/Card.jsx`:
```css
.glass-card {
  @apply glass rounded-[18px] shadow-card;
}
.glass-card-hover {
  @apply glass-card hover:border-border-secondary transition-all duration-300 hover:-translate-y-[3px];
}
```

#### Inputs
Edit in `index.css` (`.input-field` class):
```css
.input-field {
  @apply w-full bg-card-secondary border border-border-primary rounded-xl px-4 py-3 ...;
}
```

#### Borders
Edit in `tailwind.config.js` under `border` colors.

#### Shadows
Edit in `tailwind.config.js` under `boxShadow`:
```javascript
boxShadow: {
  'glow': '0 0 20px rgba(0, 245, 195, 0.15)',
  'glow-hover': '0 0 30px rgba(0, 245, 195, 0.35)',
  'card': '0 4px 24px rgba(0, 0, 0, 0.3)'
}
```

#### Typography
Edit in `tailwind.config.js` under `fontFamily` or use Tailwind's default font scale.

#### Layout
Edit grid/flex classes directly in component JSX files.

#### Grid
Edit grid classes in component JSX files:
```jsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
```

#### Responsive Design
Use Tailwind responsive prefixes:
- `sm:` - 640px and up
- `md:` - 768px and up
- `lg:` - 1024px and up
- `xl:` - 1280px and up

#### Spacing
Edit spacing classes in component JSX files (`p-6`, `m-4`, `gap-6`, etc.).

#### Animations
Edit in `tailwind.config.js` under `animation` and `keyframes`, or use Framer Motion in components.

---

### tailwind.config.js
**Location:** `tailwind.config.js`

**What it controls:**
- Color palette customization
- Custom shadows
- Custom animations
- Design tokens

**Which pages use it:** All pages (via Tailwind)

**Which components depend on it:** All components

---

## 6. Design Map - How to Modify the UI

### Navbar
**File to Edit:** `src/components/layout/Navbar.jsx`

**What to change:**
- Logo: Lines 25-35 (Shield icon + text)
- Navigation items: Lines 10-16 (navItems array)
- Styling: Lines 21-22 (glass, border classes)
- Height: Line 23 (h-16)
- Mobile menu: Lines 71-99

---

### Footer
**File to Edit:** `src/components/layout/Footer.jsx`

**What to change:**
- Brand section: Lines 10-18
- Quick links: Lines 20-28
- Social icons: Lines 32-47
- Styling: Lines 6-7 (glass, border classes)

---

### Hero Section
**File to Edit:** `src/pages/Landing.jsx`

**What to change:**
- Hero content: Lines 14-90
- Badge: Lines 21-29
- Title: Lines 31-38
- Description: Lines 40-47
- CTA buttons: Lines 49-68
- Illustration: Lines 92-145

---

### Upload Card
**File to Edit:** `src/components/ui/UploadCard.jsx`

**What to change:**
- Icon: Line 2 (Upload icon import)
- Title: Line 42 (title prop)
- Drag zone styling: Lines 69-76
- File preview: Lines 45-67
- Card styling: Line 41 (className prop)

---

### Secret Message Card
**File to Edit:** `src/components/ui/MessageCard.jsx`

**What to change:**
- Icon: Line 2 (MessageSquare icon import)
- Title: Line 10 (title prop)
- Textarea rows: Line 18
- Character counter: Lines 21-30
- Card styling: Line 9 (className prop)

---

### Password Card
**File to Edit:** `src/components/ui/PasswordCard.jsx`

**What to change:**
- Icon: Line 2 (Lock icon import)
- Title: Line 33 (title prop)
- Validation rules: Lines 24-29
- Strength indicator: Lines 43-69
- Card styling: Line 32 (className prop)

---

### Action Card
**File to Edit:** `src/components/ui/ActionCard.jsx`

**What to change:**
- Button height: Line 27 (h-[68px])
- Button styling: Lines 24-42
- Error display: Lines 18-22
- Card styling: Line 17 (className prop)

---

### Buttons
**File to Edit:** `src/components/ui/Button.jsx`

**What to change:**
- Variants: Lines 7-12 (primary, secondary, outline, danger)
- Base styles: Line 5
- Animation: Lines 16-17 (scale values)
- Gradient: Line 8 (from-accent-primary to-accent-secondary)

---

### Icons
**File to Edit:** Individual component files

**What to change:**
- Import icons from 'lucide-react' at top of file
- Replace icon component in JSX

---

### Colors
**File to Edit:** `tailwind.config.js`

**What to change:**
- Background colors: Lines 11-15
- Card colors: Lines 17-21
- Accent colors: Lines 23-27
- Text colors: Lines 33-37
- Border colors: Lines 39-42

---

### Background
**File to Edit:** `tailwind.config.js` (bg-primary color) or individual page JSX

**What to change:**
- Global background: `tailwind.config.js` line 12
- Page-specific background: Page JSX className (e.g., `bg-bg-primary`)

---

### Typography
**File to Edit:** `tailwind.config.js` or component JSX files

**What to change:**
- Font sizes: Use Tailwind classes (text-sm, text-base, text-xl, etc.)
- Font weights: Use Tailwind classes (font-normal, font-semibold, font-bold)
- Text colors: Use Tailwind color classes (text-text-primary, text-text-secondary)

---

### Card Spacing
**File to Edit:** `src/components/ui/Card.jsx` or individual card components

**What to change:**
- Card padding: `Card.jsx` line 10 (p-7 = 28px)
- Grid gap: Page JSX (gap-6 = 24px)
- Margin bottom: Page JSX (mb-6 = 24px)

---

### Card Borders
**File to Edit:** `tailwind.config.js` (border colors) or `src/index.css` (.glass class)

**What to change:**
- Border color: `tailwind.config.js` line 40
- Border width: `index.css` line 13 (border class)
- Border radius: `index.css` line 17 (rounded-[18px])

---

### Border Radius
**File to Edit:** `src/index.css` (.glass-card class) or component JSX

**What to change:**
- Global card radius: `index.css` line 17 (rounded-[18px])
- Component-specific: Add rounded classes in JSX

---

### Hover Effects
**File to Edit:** `src/index.css` (.glass-card-hover class) or component JSX

**What to change:**
- Card hover: `index.css` line 21 (hover:border-border-secondary, hover:-translate-y-[3px])
- Button hover: `Button.jsx` line 8 (hover:opacity-90)

---

### Responsive Layout
**File to Edit:** Individual page JSX files

**What to change:**
- Grid columns: Use responsive prefixes (grid-cols-1 lg:grid-cols-2)
- Padding: Use responsive prefixes (px-4 sm:px-6 lg:px-8)
- Font sizes: Use responsive prefixes (text-5xl md:text-6xl)

---

### Mobile Layout
**File to Edit:** Individual page JSX files

**What to change:**
- Mobile-first approach: Base styles for mobile, add prefixes for larger screens
- Mobile menu: `Navbar.jsx` lines 61-99
- Mobile grid: Use grid-cols-1 as base

---

### Desktop Layout
**File to Edit:** Individual page JSX files

**What to change:**
- Add lg: or xl: prefixes for desktop-specific styles
- Desktop navigation: `Navbar.jsx` lines 37-59
- Desktop grid: Use lg:grid-cols-2

---

## 7. Component Relationships

### HideMessage Page Hierarchy
```
HideMessage
├── Navbar (from layout)
├── Side Badges (inline)
├── Hero Section (inline)
├── Grid Container
│   ├── UploadCard
│   │   ├── Card
│   │   └── SectionHeader
│   ├── MessageCard
│   │   ├── Card
│   │   ├── SectionHeader
│   │   └── Textarea
│   ├── PasswordCard
│   │   ├── Card
│   │   ├── SectionHeader
│   │   └── PasswordInput
│   └── ActionCard
│       ├── Card
│       └── Button
├── SecurityInfoBar
└── Footer (from layout)
```

### ExtractMessage Page Hierarchy
```
ExtractMessage
├── Navbar (from layout)
├── Side Badges (inline)
├── Hero Section (inline)
├── Grid Container
│   ├── UploadCard
│   │   ├── Card
│   │   └── SectionHeader
│   ├── ActionCard
│   │   ├── Card
│   │   └── Button
│   ├── PasswordCard
│   │   ├── Card
│   │   ├── SectionHeader
│   │   └── PasswordInput
│   └── Card (Security Note)
├── SecurityInfoBar
└── Footer (from layout)
```

### Landing Page Hierarchy
```
Landing
├── Navbar (from layout)
├── Hero Section
│   ├── Badge (inline)
│   ├── Title
│   ├── Description
│   ├── CTA Buttons
│   │   └── Button
│   └── Features
├── Illustration (inline)
└── Footer (from layout)
```

### Component Ownership
- **Card** is owned by all card components (UploadCard, MessageCard, PasswordCard, ActionCard)
- **SectionHeader** is owned by all card components
- **Button** is owned by ActionCard, Landing, Contact
- **Input/Textarea/PasswordInput** are owned by their respective cards
- **Navbar/Footer** are owned by App (layout level)

---

## 8. Styling Flow

### Style Hierarchy
```
App (main.jsx)
  ↓ imports index.css
  ↓
Page (e.g., HideMessage.jsx)
  ↓ uses Tailwind classes
  ↓
Component (e.g., UploadCard.jsx)
  ↓ uses Tailwind classes + custom className
  ↓
index.css
  ↓ defines utility classes (.glass, .glass-card, .btn-primary, etc.)
  ↓
tailwind.config.js
  ↓ defines design tokens (colors, shadows, animations)
```

### Style Override Order
1. **Tailwind base styles** (lowest priority)
2. **Tailwind utility classes** (medium priority)
3. **Custom CSS classes from index.css** (high priority)
4. **Inline styles** (highest priority - rarely used)

### How Styles Cascade
- Global styles from `index.css` apply to all components
- Component-specific Tailwind classes override global styles where they conflict
- Custom className props can add or override styles
- No CSS modules are used - everything is global or utility-based

---

## 9. Design Tokens

### Colors
**Location:** `tailwind.config.js` lines 9-42

```javascript
// Background
bg-primary: '#070B12'      // Main page background
bg-secondary: '#0E131B'    // Secondary background

// Cards
card-primary: '#0F172A'     // Main card background
card-secondary: '#1B2234'   // Input/secondary card background

// Accent (Teal/Cyan)
accent-primary: '#00E5C2'   // Primary accent color
accent-secondary: '#00BFA5' // Secondary accent (gradient end)

// Text
text-primary: '#F5F7FA'     // Main text color
text-secondary: '#94A3B8'   // Secondary text (labels, descriptions)
text-muted: '#6D7788'       // Muted text (placeholders, hints)

// Status
success: '#00E5C2'          // Success state
warning: '#FFC857'          // Warning state
danger: '#FF5D73'           // Error state

// Border
border-primary: 'rgba(0, 245, 195, 0.12)'  // Main border color
border-secondary: 'rgba(0, 245, 195, 0.35)' // Hover border color
```

### Font Sizes
**Location:** Tailwind default scale (not customized in config)

```javascript
text-xs: 0.75rem    (12px)
text-sm: 0.875rem   (14px)
text-base: 1rem     (16px)
text-lg: 1.125rem   (18px)
text-xl: 1.25rem    (20px)
text-2xl: 1.5rem    (24px) - Card titles
text-3xl: 1.875rem  (30px)
text-4xl: 2.25rem   (36px)
text-5xl: 3rem      (48px)
text-6xl: 3.75rem   (60px) - Page titles
text-7xl: 4.5rem    (72px)
```

### Border Radius
**Location:** `src/index.css` line 17

```css
rounded-[18px]  // Cards (18px border radius)
rounded-xl      // Buttons, inputs (12px)
rounded-full    // Badges, icons (50%)
```

### Shadows
**Location:** `tailwind.config.js` lines 47-50

```javascript
shadow-glow: '0 0 20px rgba(0, 245, 195, 0.15)'
shadow-glow-hover: '0 0 30px rgba(0, 245, 195, 0.35)'
shadow-card: '0 4px 24px rgba(0, 0, 0, 0.3)'
```

### Spacing
**Location:** Tailwind default scale (not customized)

```javascript
p-4: 16px
p-6: 24px
p-7: 28px  // Card padding
p-8: 32px

gap-4: 16px
gap-6: 24px  // Grid gap

mb-4: 16px
mb-6: 24px
mb-8: 32px
mb-12: 48px
mb-16: 64px
```

### Animation Durations
**Location:** `tailwind.config.js` lines 52-66

```javascript
duration-300: 300ms  // Default transition
duration-500: 500ms  // Slower transitions
duration-800: 800ms  // Page load animations
```

### Hardcoded Values
The following values are currently hardcoded in component files:
- Button height: `h-[68px]` in ActionCard.jsx line 27
- Textarea rows: `rows={8}` in MessageCard.jsx line 18
- Max page width: `max-w-[1600px]` in page JSX files
- Container padding: `px-8` (32px) in page JSX files

---

## 10. Assets

### Icons
**Location:** Lucide React library (npm package)

**How to use:**
```javascript
import { Shield, Lock, Upload } from 'lucide-react';
<Shield className="w-5 h-5" />
```

**No local icon files** - all icons are from Lucide React.

### Images
**Location:** `src/assets/` (currently empty)

**No local images** - the project uses CSS effects and icons instead of images.

### Logos
**Location:** No logo file - logo is rendered using Shield icon + text

**Logo rendering:** Navbar.jsx lines 25-35, Footer.jsx lines 10-18

### Fonts
**Location:** System fonts (no custom font files)

**Font stack:** Tailwind default (sans-serif)

---

## 11. Best Places to Edit

| Task | File to Edit |
|------|--------------|
| Change navbar | `src/components/layout/Navbar.jsx` |
| Change footer | `src/components/layout/Footer.jsx` |
| Change upload card | `src/components/ui/UploadCard.jsx` |
| Change message card | `src/components/ui/MessageCard.jsx` |
| Change password card | `src/components/ui/PasswordCard.jsx` |
| Change action card | `src/components/ui/ActionCard.jsx` |
| Change button style | `src/components/ui/Button.jsx` |
| Change card color | `tailwind.config.js` (card-primary) |
| Change card padding | `src/components/ui/Card.jsx` (p-7) |
| Change card border radius | `src/index.css` (.glass-card) |
| Change spacing | Component JSX files (gap, padding classes) |
| Change typography | `tailwind.config.js` or component JSX |
| Change colors | `tailwind.config.js` (colors section) |
| Change background | `tailwind.config.js` (bg-primary) |
| Change shadows | `tailwind.config.js` (boxShadow section) |
| Change animations | `tailwind.config.js` (animation section) |
| Change security bar | `src/components/ui/SecurityInfoBar.jsx` |
| Change section header | `src/components/common/SectionHeader.jsx` |
| Change input style | `src/index.css` (.input-field) |
| Change textarea style | `src/index.css` (.input-field) |
| Change page layout | Page JSX files (grid classes) |
| Change hero section | `src/pages/Landing.jsx` |
| Change responsive breakpoints | Tailwind classes in component JSX |

---

## 12. Dependencies

### UI-Related Libraries

| Library | Version | Purpose | Where Used |
|---------|---------|---------|------------|
| React | 18.3.1 | UI library | All components |
| React DOM | 18.3.1 | React rendering | main.jsx |
| React Router DOM | 6.23.1 | Client-side routing | App.jsx, Navbar.jsx |
| Tailwind CSS | 3.4.3 | Utility-first CSS | All components (via classes) |
| Framer Motion | 11.2.10 | Animations | Card.jsx, Button.jsx, Navbar.jsx, Landing.jsx, About.jsx, Contact.jsx |
| Lucide React | 0.379.0 | Icon library | All components with icons |

### Where Each Library is Used

**React:**
- All .jsx files - component structure and state management

**React Router DOM:**
- App.jsx - Routes configuration
- Navbar.jsx - Navigation links and active route detection

**Tailwind CSS:**
- All components - styling via utility classes
- index.css - custom utility classes
- tailwind.config.js - design tokens

**Framer Motion:**
- Card.jsx - fade-in animation
- Button.jsx - hover/tap scale animations
- Navbar.jsx - mobile menu animation, active indicator
- Landing.jsx - hero section animations, floating elements
- About.jsx - card fade-in animations
- Contact.jsx - card slide-in animations

**Lucide React:**
- All components with icons - provides consistent icon set

---

## 13. Responsive Layout

### Breakpoints
**Location:** Tailwind default breakpoints

```javascript
sm: 640px   // Small tablets
md: 768px   // Tablets
lg: 1024px  // Laptops/desktops
xl: 1280px  // Large desktops
```

### Media Queries
**Approach:** Mobile-first with Tailwind responsive prefixes

**Example:**
```jsx
<div className="px-4 sm:px-6 lg:px-8">
  {/* 16px padding on mobile, 24px on tablet, 32px on desktop */}
</div>
```

### Flex
**Used for:**
- Navbar layout (horizontal on desktop, vertical on mobile)
- Card internal layout (vertical stacking)
- Button content (icon + text alignment)

**Example:**
```jsx
<div className="flex items-center justify-between">
  {/* Horizontal layout with centered items */}
</div>
```

### Grid
**Used for:**
- Main page layout (2-column grid on desktop)
- Card grids (About page technologies)
- SecurityInfoBar (5-column grid)

**Example:**
```jsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
  {/* 1 column on mobile, 2 columns on desktop */}
</div>
```

### Responsive Patterns

**Desktop (lg: and above):**
- 2-column grid for main content
- Horizontal navigation
- Full-width containers with max-width 1600px

**Tablet (md:):**
- Same as desktop but with adjusted padding
- Some components may stack vertically

**Mobile (default):**
- Single column layout
- Hamburger menu for navigation
- Reduced padding
- Stacked cards

---

## 14. Tips for Future UI Editing

### General Guidelines

1. **Always test responsive behavior** - Changes on desktop may break mobile layout
2. **Use Tailwind classes instead of custom CSS** - Maintains consistency
3. **Keep component props minimal** - Pass only necessary data
4. **Preserve existing functionality** - Don't modify business logic when editing UI
5. **Test animations** - Ensure they don't cause performance issues

### Color Changes
1. Edit colors in `tailwind.config.js` first
2. Check all components that use the color
3. Test contrast ratios for accessibility
4. Update gradient endpoints if changing accent colors

### Layout Changes
1. Start with grid/flex classes in page JSX
2. Test on mobile first, then tablet, then desktop
3. Ensure max-width containers are preserved
4. Check for overflow issues

### Component Modifications
1. Read the entire component file before editing
2. Understand props and state
3. Preserve existing animations
4. Test with all prop combinations

### Styling Safety
1. Never modify `index.css` without understanding the impact
2. Use className props for component-specific styles
3. Avoid inline styles (use Tailwind instead)
4. Keep custom CSS to a minimum

### Breaking Changes to Avoid
1. Don't remove required props from components
2. Don't change component file names (affects imports)
3. Don't remove Tailwind classes without replacement
4. Don't modify routing in App.jsx without updating Navbar

### Testing Checklist
After UI changes, verify:
- [ ] Mobile layout (resize browser to < 768px)
- [ ] Tablet layout (768px - 1024px)
- [ ] Desktop layout (> 1024px)
- [ ] All animations work smoothly
- [ ] No console errors
- [ ] All buttons are clickable
- [ ] Forms are accessible
- [ ] Colors have good contrast

### Common Pitfalls
1. **Forgot to add responsive prefixes** - Mobile layout breaks on desktop
2. **Changed color in one place only** - Inconsistent colors across app
3. **Modified component props** - Parent components break
4. **Removed animation classes** - Lost smooth transitions
5. **Hardcoded pixel values** - Breaks responsive design

### Best Practices
1. **Copy existing patterns** - Look at similar components before creating new ones
2. **Use utility classes consistently** - Don't mix random values
3. **Keep changes minimal** - Small edits are easier to debug
4. **Commit frequently** - Easier to revert if something breaks
5. **Document custom changes** - Add comments for non-obvious styling

---

## Quick Reference

### Common Tailwind Classes Used

**Spacing:**
- `p-7` - 28px padding (cards)
- `px-8` - 32px horizontal padding (containers)
- `gap-6` - 24px gap (grid)
- `mb-6` - 24px bottom margin

**Layout:**
- `grid grid-cols-1 lg:grid-cols-2` - Responsive 2-column grid
- `flex flex-col` - Vertical flex layout
- `items-center` - Center items vertically
- `justify-center` - Center items horizontally

**Colors:**
- `bg-bg-primary` - Main background
- `bg-card-primary` - Card background
- `text-text-primary` - Main text
- `text-text-secondary` - Secondary text
- `text-accent-primary` - Accent text

**Borders:**
- `border-border-primary` - Main border
- `rounded-[18px]` - Card border radius
- `rounded-xl` - Input/button border radius

**Effects:**
- `glass` - Glass morphism effect
- `shadow-glow` - Neon glow effect
- `hover:-translate-y-[3px]` - Lift on hover

---

## Conclusion

This documentation covers the entire frontend UI structure of the SecureStego project. When modifying the UI, always refer to this guide to understand the component hierarchy, styling flow, and best practices for making changes without breaking functionality.

For any questions about specific components or styling, refer to the relevant section in this documentation or examine the source code directly.
