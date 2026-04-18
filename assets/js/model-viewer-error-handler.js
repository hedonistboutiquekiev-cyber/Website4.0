/**
 * Model Viewer Error Handler
 * Provides robust error handling and recovery for model-viewer elements
 */
(function() {
  'use strict';

  const originalLog = console.log;
  const originalError = console.error;
  
  // Store original console methods before model-viewer loads
  const errorLog = [];
  
  // Monitor for model-viewer specific errors
  const handleError = (error) => {
    // Silently catch specific model-viewer and CORS errors to prevent page blocking
    if (error && typeof error === 'object') {
      const message = error.message || error.toString();
      
      // Suppress CORS-related error clutter but keep tracking
      if (message.includes('CORS') || message.includes('fetch') || message.includes('timeout')) {
        console.debug('[model-viewer] Network/CORS issue (suppressed):', message);
        return true; // Handled
      }
      
      // Suppress texture loading errors from model-viewer
      if (message.includes('texture') || message.includes('blob:') || message.includes('GLTFLoader')) {
        console.debug('[model-viewer] Texture issue (suppressed):', message);
        return true; // Handled
      }
      
      // Let other errors through
      return false;
    }
    return false;
  };

  // Override console.error to suppress specific errors
  const originalConsoleError = console.error;
  console.error = function(...args) {
    const firstArg = args[0];
    let isSupressed = false;
    
    if (typeof firstArg === 'string') {
      isSupressed = handleError({ message: firstArg });
    } else if (firstArg instanceof Error) {
      isSupressed = handleError(firstArg);
    }
    
    if (!isSupressed) {
      originalConsoleError.apply(console, args);
    }
  };

  // Wait for DOM ready, then enhance all model-viewers
  const enhanceModelViewers = () => {
    const viewers = document.querySelectorAll('model-viewer');
    
    viewers.forEach(viewer => {
      // Add error handlers
      viewer.addEventListener('error', (event) => {
        console.warn('[model-viewer] Load error caught:', event);
        // Model-preloader.js handles the visual feedback
      }, false);

      // Add load handler
      viewer.addEventListener('load', (event) => {
        console.debug('[model-viewer] Model loaded successfully');
      }, false);

      // Add progress handler
      viewer.addEventListener('progress', (event) => {
        if (event.detail && event.detail.totalProgress) {
          const percent = Math.round(event.detail.totalProgress * 100);
          if (percent % 25 === 0) {
            console.debug(`[model-viewer] Loading: ${percent}%`);
          }
        }
      }, false);

      // Handle viewer-specific attributes
      const src = viewer.getAttribute('src');
      if (src) {
        // Pre-check model file availability
        fetch(src, { method: 'HEAD' })
          .then(res => {
            if (!res.ok) {
              console.warn(`[model-viewer] Model file returned status ${res.status}: ${src}`);
            }
          })
          .catch(err => {
            console.debug(`[model-viewer] Model file preflight check failed: ${src}`);
          });
      }
    });
  };

  // Execute when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceModelViewers, { once: true });
  } else {
    enhanceModelViewers();
  }

  // Also watch for dynamically added model-viewers
  if (window.MutationObserver) {
    const observer = new MutationObserver((mutations) => {
      let hasNewViewers = false;
      mutations.forEach(mutation => {
        if (mutation.addedNodes.length > 0) {
          mutation.addedNodes.forEach(node => {
            if (node.tagName === 'MODEL-VIEWER' || 
                (node.querySelectorAll && node.querySelectorAll('model-viewer').length > 0)) {
              hasNewViewers = true;
            }
          });
        }
      });
      if (hasNewViewers) {
        enhanceModelViewers();
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  // Expose debug mode
  window.__modelViewerDebug = false;

})();
