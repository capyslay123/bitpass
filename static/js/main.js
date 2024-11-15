"use strict";

const passwordField = document.querySelectorAll("input[type='password']");
const showPassword = document.querySelectorAll(".show-password-ic");
const hidePassword = document.querySelectorAll(".hide-password-ic");

const categoriesModal = document.querySelector(".add-categories-modal");
const openModalCategories = document.querySelectorAll(".open-modal-categories");
const closeModalCategories = document.querySelector(".close-modal-categories");

const deleteModal = document.querySelector(".delete-modal");
const deleteModalForm = document.querySelector(".delete-modal-form");
const openModalDelete = document.querySelectorAll(".delete-password-ic");
const closeModalDelete = document.querySelector(".close-modal-delete");

// FILTER CATEGORY FOR DESKTOP
const filterCategory = document.querySelector(".filter-category");
const categoryChevron = document.querySelector(".category-chevron");
const categoryContent = document.querySelector(".category-content");

// FILTER CATEGORY FOR MOBILE
const filterCategoryMobile = document.querySelector(".filter-category-mobile");
const categoryChevronMobile = document.querySelector(
  ".category-chevron-mobile"
);
const categoryContentMobile = document.querySelector(
  ".category-content-mobile"
);

const userMenu = document.querySelector(".user-menu");
const userMenuChevron = document.querySelector(".user-menu-chevron");
const userMenuContent = document.querySelector(".user-menu-content");

const navContentMobile = document.querySelector(".nav-content-mobile");
const hamburgerIcon = document.querySelector(".hamburger-ic");
const closeIcon = document.querySelector(".close-ic");
const navLinkMobile = document.querySelector(".nav-link-mobile");

const addPasswordCancel = document.querySelector(".add-password-cancel");

const accountPassword = document.querySelectorAll(".account-password");
const accountPasswordBullet = document.querySelectorAll(
  ".account-password-bullet"
);
const showAccountPassword = document.querySelectorAll(".show-account-password");
const hideAccountPassword = document.querySelectorAll(".hide-account-password");

const accountUsername = document.querySelectorAll(".account-username");
const accountEmail = document.querySelectorAll(".account-email");
const accountUsernameCopy = document.querySelectorAll(".account-username-copy");
const accountEmailCopy = document.querySelectorAll(".account-email-copy");
const accountPasswordCopy = document.querySelectorAll(".account-password-copy");

const accountTitle = document.querySelector(".account-title");
const accountURL = document.querySelector(".account-url");
const accountLogo = document.querySelector(".account-logo");
const accountPasswordID = document.querySelectorAll(".account-password-id");

const toast = document.querySelector(".toast");

const cancelDelete = document.querySelector(".cancel-delete");
const previousURL = document.querySelector(".previous-url");

// COPY TEXT ELEMENT TO CLIPBOARD
function copyToClipboard(el, msgEl) {
  /*
  IT TAKES THE TEXT CONTENT OF HTML ELEMENT AND CREATES A TEXTAREA ELEMENT, IT TAKES TEXT CONTENT VALUE AND COPY IT TO THE TEXT AREA SO THAT WE CAN SELECT THE TEXT AND USE THE EXECUTE COMMAND (IN THIS CASE COPY COMMAND) FUNCTION ON THE CURRENT SELECTION AFTER COPYING THE TEXT TO THE CLIPBOARD IT REMOVES THE PREVIOULSY ADDED TEXTAREA ELEMENT.
  */
  const textToCopy = el.textContent.trim();
  const textEl = document.createElement("textarea");
  textEl.value = textToCopy;
  document.body.appendChild(textEl);
  textEl.select();
  document.execCommand("copy");
  msgEl.classList.add("active"); // SHOWS THE COPIED MESSAGE
  document.body.removeChild(textEl);

  // REMOVES THE COPIED MESSAGE
  setTimeout(() => {
    msgEl.classList.remove("active");
  }, 800);
}

// MOBILE NAVBAR OPEN
if (hamburgerIcon) {
  hamburgerIcon.addEventListener("click", () => {
    hamburgerIcon.style.display = "none";
    navContentMobile.style.height = "10rem";
    closeIcon.style.display = "block";
    navLinkMobile.style.display = "inline";
  });

  // MOBILE NAVBAR CLOSE
  closeIcon.addEventListener("click", () => {
    closeIcon.style.display = "none";
    navContentMobile.style.height = "0";
    hamburgerIcon.style.display = "block";
    navLinkMobile.style.display = "none";
  });
}

for (let i = 0; i < passwordField.length; i++) {
  // TOGGLE PASSWORD - SHOW PASSWORD
  showPassword[i].addEventListener("click", () => {
    passwordField[i].type = "text";
    hidePassword[i].style.display = "block";
    showPassword[i].style.display = "none";
  });

  // TOGGLE PASSWORD - HIDE PASSWORD
  hidePassword[i].addEventListener("click", () => {
    passwordField[i].type = "password";
    hidePassword[i].style.display = "none";
    showPassword[i].style.display = "block";
  });
}

// CATEGORIES MODAL
for (let i = 0; i < openModalCategories.length; i++) {
  // OPEN MODAL
  openModalCategories[i].addEventListener("click", () => {
    categoriesModal.classList.add("open");
  });
}
// CLOSE MODAL
if (closeModalCategories) {
  closeModalCategories.addEventListener("click", (e) => {
    e.preventDefault();
    categoriesModal.classList.remove("open");
  });
}

// DELETE MODAL
for (let i = 0; i < openModalDelete.length; i++) {
  // OPEN MODAL
  openModalDelete[i].addEventListener("click", () => {
    deleteModal.classList.add("open");
    // SETTING FORM ACTION TO A URL THROUGH WHICH WE CAN DELETE ACCOUNT PASSWORD (BASCIALLY SENDING THE ID OF THE ACCOUNT PASSWORD OBJECT THROGH URL)
    deleteModalForm.action = `/delete-password/${accountPasswordID[i].textContent}/`;
  });
}
// CLOSE MODAL
if (closeModalDelete) {
  closeModalDelete.addEventListener("click", (e) => {
    e.preventDefault();
    deleteModal.classList.remove("open");
  });
}

// FILTER CATEGORY DROP DOWN FOR DESKTOP
if (filterCategory) {
  filterCategory.addEventListener("click", () => {
    if (categoryContent.classList.contains("show")) {
      categoryContent.classList.remove("show");
      categoryChevron.style.transform = "rotate(0)";
    } else {
      categoryChevron.style.transform = "rotate(180deg)";
      categoryContent.classList.add("show");
    }
  });

  // USER CLICK OUTSIDE WINDOW ---> CLOSE DROPDOWN MENU FOR DESKTOP
  window.onclick = (e) => {
    if (
      !e.target.matches(".filter-category span") &&
      !e.target.matches(".filter-category img")
    ) {
      if (categoryContent.classList.contains("show")) {
        categoryContent.classList.remove("show");
        categoryChevron.style.transform = "rotate(0)";
      }
    }
  };
}

// FILTER CATEGORY DROP DOWN FOR MOBILE
if (filterCategoryMobile) {
  filterCategoryMobile.addEventListener("click", () => {
    if (categoryContentMobile.classList.contains("show")) {
      categoryContentMobile.classList.remove("show");
      categoryChevronMobile.style.transform = "rotate(0)";
    } else {
      categoryChevronMobile.style.transform = "rotate(180deg)";
      categoryContentMobile.classList.add("show");
    }
  });

  // USER CLICK OUTSIDE WINDOW ---> CLOSE DROPDOWN MENU FOR DESKTOP
  window.onclick = (e) => {
    if (
      !e.target.matches(".filter-category-mobile span") &&
      !e.target.matches(".filter-category-mobile img")
    ) {
      if (categoryContentMobile.classList.contains("show")) {
        categoryContentMobile.classList.remove("show");
        categoryChevronMobile.style.transform = "rotate(0)";
      }
    }
  };
}

// USER DROP DOWN MENU
if (userMenu) {
  userMenu.addEventListener("click", () => {
    if (userMenuContent.classList.contains("show")) {
      userMenuContent.classList.remove("show");
      userMenuChevron.style.transform = "rotate(0)";
    } else {
      userMenuContent.classList.add("show");
      userMenuChevron.style.transform = "rotate(180deg)";
    }
  });

  // USER CLICK OUTSIDE WINDOW ---> USER DROPDOWN MENU
  window.onclick = (e) => {
    if (
      !e.target.matches(".user-menu") &&
      !e.target.matches(".user-menu span") &&
      !e.target.matches(".user-menu img") &&
      !e.target.matches(".user-menu div")
    ) {
      if (userMenuContent.classList.contains("show")) {
        userMenuContent.classList.remove("show");
        userMenuChevron.style.transform = "rotate(0)";
      }
    }
  };
}

// DISABLE SUBMITTING ADD PASSWORD FORM THROUGH CANCEL BUTTON
if (addPasswordCancel) {
  addPasswordCancel.addEventListener("click", (e) => {
    e.preventDefault();
    window.location.href = "/vault/";
  });
}

// TOGGLE ACCOUNT'S PASSWORD
if (accountPassword) {
  for (let i = 0; i < accountPassword.length; i++) {
    showAccountPassword[i].addEventListener("click", () => {
      accountPasswordBullet[i].style.display = "none";
      accountPassword[i].style.display = "block";
      showAccountPassword[i].style.display = "none";
      hideAccountPassword[i].style.display = "block";
    });

    hideAccountPassword[i].addEventListener("click", () => {
      accountPasswordBullet[i].style.display = "flex";
      accountPassword[i].style.display = "none";
      hideAccountPassword[i].style.display = "none";
      showAccountPassword[i].style.display = "block";
    });
  }
}

// COPY ACCOUNT DETAILS TO CLIPBOARD
if (accountPassword) {
  for (let i = 0; i < accountPassword.length; i++) {
    // COPY USERNAME
    if (accountUsernameCopy[i]) {
      accountUsernameCopy[i].addEventListener("click", () => {
        copyToClipboard(accountUsername[i], accountUsernameCopy[i].parentNode);
      });
    }

    // COPY EMAIL
    if (accountEmail[i]) {
      accountEmailCopy[i].addEventListener("click", () => {
        copyToClipboard(accountEmail[i], accountEmailCopy[i].parentNode);
      });
    }

    // COPY PASSWORD
    accountPasswordCopy[i].addEventListener("click", () => {
      copyToClipboard(accountPassword[i], accountPasswordCopy[i].parentNode);
    });
  }
}

// SHOWS ACCOUNT LOGO BASED ON TITLE, ONLY SHOWS IF LOGO NOT AVAILABLE FROM URL OR URL NOT AVAILABLE
if (accountTitle) {
  accountTitle.addEventListener("blur", () => {
    if (accountTitle.value) {
      // THIS IF STATEMENT ENSURES THAT LOGO AVAILABLE FROM URL OR NOT
      if (!document.querySelector(".password-logo")) {
        // ONLY SHOWS THE INITIAL OF THE ACCOUNT NAME AS LOGO
        let acronym = "";
        const textArr = accountTitle.value.split(" ");

        for (let i = 0; i < textArr.length; i++) {
          acronym = acronym + textArr[i][0];
        }

        accountLogo.textContent = acronym;
        acronym = "";
      }
    }
  });
}

// SHOWS ACCOUNT LOGO BASED ON URL PROVIDED
if (accountURL) {
  accountURL.addEventListener("blur", () => {
    if (accountURL.value) {
      // USES CLEARBIT API TO SHOW LOGO BASED ON URL
      const URL = "https://logo.clearbit.com/" + accountURL.value;

      // INSERT IMAGE ON HTML USING API URL AS SRC OF THE IMAGE
      accountLogo.innerHTML = `<img src="${URL}" alt="Logo" class="w-3/4 password-logo rounded-full"/>`;

      // IF IMAGE IS FAILED TO FETCH OR WRONG URL THEN SHOWS ERROR
      document.querySelector(".password-logo").onerror = () => {
        accountLogo.innerHTML = `<p class="text-xs text-center mx-5">Wrong URL or Fetch Error</p>`;
      };
    }
  });
}

// REMOVES THE SUCCESS OR ERROR TOAST AFTER 1s UPON SUBMITTING ADD CATEGORY FORM
if (toast) {
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.bottom = "0";
  }, 1300);
}

if (cancelDelete) {
  cancelDelete.addEventListener("click", (e) => {
    e.preventDefault();
    window.location = `${previousURL.textContent}`;
  });
}
