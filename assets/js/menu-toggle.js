/**
 * MENU TOGGLE - Mobile & Desktop Dropdown Handler
 * Optimized for performance and accessibility
 */

(function initDropdowns() {
  'use strict';

  const CONFIG = {
    desktop_breakpoint: 1024,
    debug: false
  };

  let initialized = false;
  let lastWindowWidth = window.innerWidth;

  /**
   * Initialize dropdown menu handlers
   */
  function init() {
    if (initialized) return;
    initialized = true;

    const nav = document.querySelector('.main-nav');
    if (!nav) {
      requestAnimationFrame(init);
      return;
    }

    const dropdowns = nav.querySelectorAll('.dropdown');
    if (dropdowns.length === 0) {
      log('No dropdowns found');
      return;
    }

    // Setup each dropdown
    dropdowns.forEach(dropdown => {
      setupDropdown(dropdown);
    });

    // Setup event delegation
    setupDocumentListeners();
    setupWindowResize();

    log(`✅ Initialized ${dropdowns.length} dropdowns`);
  }

  /**
   * Setup individual dropdown
   */
  function setupDropdown(dropdown) {
    const trigger = dropdown.querySelector('.dropdown-trigger');
    const menu = dropdown.querySelector('.dropdown-menu');

    if (!trigger || !menu) return;

    const isDesktop = window.innerWidth >= CONFIG.desktop_breakpoint;

    if (isDesktop) {
      let closeTimeoutId = null;

      const clearCloseTimer = () => {
        if (closeTimeoutId) {
          clearTimeout(closeTimeoutId);
          closeTimeoutId = null;
        }
      };

      const openDropdown = () => {
        clearCloseTimer();
        dropdown.classList.add('active');
        trigger.setAttribute('aria-expanded', 'true');
      };

      const scheduleCloseDropdown = () => {
        clearCloseTimer();
        closeTimeoutId = setTimeout(() => {
          dropdown.classList.remove('active');
          trigger.setAttribute('aria-expanded', 'false');
          closeTimeoutId = null;
        }, 2000);
      };

      dropdown.addEventListener('mouseenter', openDropdown);
      dropdown.addEventListener('mouseleave', scheduleCloseDropdown);

      menu.addEventListener('mouseenter', openDropdown);
      menu.addEventListener('mouseleave', scheduleCloseDropdown);

      trigger.addEventListener('click', e => e.preventDefault(), { once: false });
    } else {
      // Mobile: click to toggle
      trigger.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        toggleDropdown(dropdown, trigger, menu);
      });
    }
  }

  /**
   * Toggle dropdown visibility
   */
  function toggleDropdown(dropdown, trigger, menu) {
    const isActive = dropdown.classList.contains('active');

    // Close other dropdowns
    document.querySelectorAll('.dropdown.active').forEach(openDropdown => {
      if (openDropdown !== dropdown) {
        openDropdown.classList.remove('active');
        const openTrigger = openDropdown.querySelector('.dropdown-trigger');
        if (openTrigger) openTrigger.setAttribute('aria-expanded', 'false');
      }
    });

    // Toggle current dropdown
    if (isActive) {
      dropdown.classList.remove('active');
      trigger.setAttribute('aria-expanded', 'false');
    } else {
      dropdown.classList.add('active');
      trigger.setAttribute('aria-expanded', 'true');
    }
  }

  /**
   * Close dropdowns when clicking outside
   */
  function setupDocumentListeners() {
    document.addEventListener('click', e => {
      if (window.innerWidth < CONFIG.desktop_breakpoint) {
        const nav = document.querySelector('.main-nav');
        if (nav && !nav.contains(e.target)) {
          document.querySelectorAll('.dropdown.active').forEach(dropdown => {
            dropdown.classList.remove('active');
            const trigger = dropdown.querySelector('.dropdown-trigger');
            if (trigger) trigger.setAttribute('aria-expanded', 'false');
          });
        }
      }
    });

    // Close on Escape
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.dropdown.active').forEach(dropdown => {
          dropdown.classList.remove('active');
          const trigger = dropdown.querySelector('.dropdown-trigger');
          if (trigger) trigger.setAttribute('aria-expanded', 'false');
        });
      }
    });
  }

  /**
   * Handle window resize
   */
  function setupWindowResize() {
    window.addEventListener('resize', () => {
      const currentWidth = window.innerWidth;
      const wasDesktop = lastWindowWidth >= CONFIG.desktop_breakpoint;
      const isDesktop = currentWidth >= CONFIG.desktop_breakpoint;

      if (wasDesktop !== isDesktop) {
        document.querySelectorAll('.dropdown.active').forEach(dropdown => {
          dropdown.classList.remove('active');
          const trigger = dropdown.querySelector('.dropdown-trigger');
          if (trigger) trigger.setAttribute('aria-expanded', 'false');
        });

        lastWindowWidth = currentWidth;
        initialized = false;
        init();
      }
    });
  }

  /**
   * Debug logging
   */
  function log(message) {
    if (CONFIG.debug) {
      console.log('[MenuToggle]', message);
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    requestAnimationFrame(init);
  }
})();
