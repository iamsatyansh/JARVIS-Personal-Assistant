class JarvisError(Exception):
    """Base exception class for JARVIS-specific errors."""
    pass

class ConfigurationError(JarvisError):
    """Raised when there's a configuration-related error."""
    pass

class ServiceUnavailableError(JarvisError):
    """Raised when an external service is unavailable."""
    pass

class DatabaseError(JarvisError):
    """Raised when there's a database-related error."""
    pass

class SpeechRecognitionError(JarvisError):
    """Raised when speech recognition fails."""
    pass

class TTSError(JarvisError):
    """Raised when text-to-speech fails."""
    pass

class CircuitBreakerOpenError(JarvisError):
    """Raised when circuit breaker is open."""
    pass
