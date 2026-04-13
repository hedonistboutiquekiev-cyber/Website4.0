const WORKER_AUTH_URL = "https://albaspace-api.nncdecdgc.workers.dev/auth/google";
const WORKER_ME_URL = "https://albaspace-api.nncdecdgc.workers.dev/me";
const AUTH_RETURN_KEY = "albaspace_auth_return_to";
const AUTH_SOURCE_KEY = "albaspace_auth_source";

function login(options = {}) {
  persistAuthState(options.source || "default");
  closeAuthUi(options);
  window.location.href = WORKER_AUTH_URL;
}

async function checkUser() {
  try {
    const res = await fetch(WORKER_ME_URL, {
      credentials: "include"
    });

    if (res.ok) {
      const user = await res.json();
      console.log("Logged in:", user);

      setUserText("Hello " + (user.name || user.email || "user"));
      closeAuthUi({ closeModal: true, closeMenu: true });
      restorePendingReturnUrl();
    } else {
      console.log("Not logged in");
      setUserText("");
    }
  } catch (error) {
    console.error("Failed to check current user:", error);
    setUserText("");
  }
}

function setUserText(text) {
  const seen = new Set();
  const userElements = [
    ...document.querySelectorAll(".worker-auth-user"),
    ...document.querySelectorAll("#user")
  ].filter((element) => {
    if (!element || seen.has(element)) {
      return false;
    }
    seen.add(element);
    return true;
  });

  userElements.forEach((element) => {
    element.innerText = text;
  });
}

function persistAuthState(source) {
  try {
    sessionStorage.setItem(
      AUTH_RETURN_KEY,
      window.location.pathname + window.location.search + window.location.hash
    );
    sessionStorage.setItem(AUTH_SOURCE_KEY, source);
  } catch (error) {
    console.warn("Unable to persist auth state:", error);
  }
}

function restorePendingReturnUrl() {
  try {
    const returnTo = sessionStorage.getItem(AUTH_RETURN_KEY);
    const currentPath = window.location.pathname + window.location.search + window.location.hash;

    if (!returnTo) {
      return;
    }

    sessionStorage.removeItem(AUTH_RETURN_KEY);
    sessionStorage.removeItem(AUTH_SOURCE_KEY);

    if (returnTo !== currentPath && returnTo.startsWith("/")) {
      window.location.replace(returnTo);
    }
  } catch (error) {
    console.warn("Unable to restore auth state:", error);
  }
}

function closeAuthUi(options = {}) {
  if (options.closeMenu) {
    const menu = document.getElementById("alienMenu");
    const trigger = document.querySelector(".alien-ghost");

    if (menu) {
      menu.style.display = "none";
    }
    if (trigger) {
      trigger.setAttribute("aria-expanded", "false");
    }
  }

  if (options.closeModal) {
    const overlay = document.getElementById("signup-modal-overlay");
    if (overlay) {
      overlay.style.display = "none";
      overlay.setAttribute("aria-hidden", "true");
    }
    document.body.style.overflow = "";
  }
}

window.login = login;
window.checkUser = checkUser;

checkUser();
