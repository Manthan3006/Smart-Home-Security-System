"""
🎓 HOME SECURITY SYSTEM CONFIGURATION
Customize your home security system settings here
"""

from datetime import time

# ==================== ATTENDANCE SETTINGS ====================
REPORTING_TIME = time(10, 0)  # 10:00 AM - Change as needed
ATTENDANCE_FOLDER = "attendance_records"
PICS_FOLDER = "Pics"
ADMIN_CONFIG_FILE = "admin_config.json"

# ==================== PERFORMANCE SETTINGS ====================
# Camera optimization settings
FRAME_SKIP = 3  # Process every 3rd frame (increase for better performance)
RESIZE_FACTOR = 0.5  # Resize to 50% for processing (decrease for better performance)
FACE_RECOGNITION_TOLERANCE = 0.6  # Face matching sensitivity (0.4-0.8 recommended)
MAX_FACES_PER_FRAME = 5  # Maximum faces to process per frame

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
CAMERA_BUFFER_SIZE = 1

# ==================== UI THEME SETTINGS ====================
# Glassmorphism color scheme
GLASSMORPHISM_COLORS = {
    'primary_bg': '#0D1117',           # Main background
    'glass_bg': 'rgba(255, 255, 255, 0.1)',  # Glass panel background
    'glass_border': 'rgba(255, 255, 255, 0.2)',  # Glass panel border
    'text_primary': '#FFFFFF',          # Primary text color
    'text_secondary': '#8B949E',        # Secondary text color
    'accent_blue': '#58A6FF',          # Blue accent (buttons, highlights)
    'accent_green': '#3FB950',         # Green accent (success, present)
    'accent_red': '#F85149',           # Red accent (danger, unknown)
    'accent_orange': '#D29922'         # Orange accent (warning, late)
}

# UI Layout settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
CORNER_RADIUS = 20
BUTTON_HEIGHT = 45
CARD_PADDING = 20

# Font settings
TITLE_FONT_SIZE = 36
SUBTITLE_FONT_SIZE = 16
BUTTON_FONT_SIZE = 14
CARD_FONT_SIZE = 24

# ==================== CHART SETTINGS ====================
# Chart styling
CHART_BACKGROUND = '#161B22'
CHART_TEXT_COLOR = 'white'
CHART_COLORS = {
    'present': '#3FB950',
    'late': '#D29922',
    'absent': '#F85149',
    'primary': '#58A6FF'
}

# Chart dimensions
CHART_DPI = 100
CHART_FIGURE_SIZE = (12, 8)

# ==================== SECURITY SETTINGS ====================
# Admin settings
DEFAULT_ADMIN_PASSWORD = "admin123"  # Change this!
PASSWORD_HASH_ALGORITHM = "sha256"
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# ==================== DATA SETTINGS ====================
# Analytics settings
DEFAULT_ANALYTICS_DAYS = 30  # Days to look back for analytics
MAX_EMPLOYEES_IN_CHART = 10  # Maximum employees to show in charts
CSV_DATE_FORMAT = "%Y-%m-%d"
CSV_TIME_FORMAT = "%H:%M:%S"

# ==================== NOTIFICATION SETTINGS ====================
# Sound and notification settings
ENABLE_SOUND_NOTIFICATIONS = True
ENABLE_CONSOLE_NOTIFICATIONS = True
NOTIFICATION_VOLUME = 0.5  # 0.0 to 1.0

# ==================== EXPORT SETTINGS ====================
# Chart export settings
EXPORT_FORMATS = ['PNG', 'PDF', 'SVG']
EXPORT_DPI = 300
EXPORT_QUALITY = 95

# ==================== ADVANCED SETTINGS ====================
# Threading settings
USE_THREADING = True
THREAD_TIMEOUT = 30

# Logging settings
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "home_security.log"

# Backup settings
AUTO_BACKUP = True
BACKUP_INTERVAL_DAYS = 7
BACKUP_FOLDER = "backups"

# ==================== FEATURE FLAGS ====================
# Enable/disable features
FEATURES = {
    'glassmorphism_ui': True,
    'admin_dashboard': True,
    'employee_stats': True,
    'chart_export': True,
    'dark_mode_toggle': True,
    'animated_transitions': True,
    'hover_effects': True,
    'sound_notifications': True,
    'auto_backup': True,
    'advanced_analytics': True
}

# ==================== VALIDATION ====================
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Validate time settings
    if not isinstance(REPORTING_TIME, time):
        errors.append("REPORTING_TIME must be a datetime.time object")
    
    # Validate performance settings
    if FRAME_SKIP < 1:
        errors.append("FRAME_SKIP must be >= 1")
    
    if not 0.1 <= RESIZE_FACTOR <= 1.0:
        errors.append("RESIZE_FACTOR must be between 0.1 and 1.0")
    
    if not 0.3 <= FACE_RECOGNITION_TOLERANCE <= 0.8:
        errors.append("FACE_RECOGNITION_TOLERANCE should be between 0.3 and 0.8")
    
    # Validate UI settings
    if WINDOW_WIDTH < 800 or WINDOW_HEIGHT < 600:
        errors.append("Window dimensions should be at least 800x600")
    
    return errors

# Validate configuration on import
config_errors = validate_config()
if config_errors:
    print("⚠️ Configuration Warnings:")
    for error in config_errors:
        print(f"  - {error}")