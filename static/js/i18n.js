/**
 * Tamil / English i18n for AI Crop Recommendation
 * Usage: add data-i18n="key" on any element.
 * The switcher reads/writes the preference to localStorage("lang").
 */

const TRANSLATIONS = {
  en: {
    /* ── Navbar ── */
    "nav.brand":       "AI Crop Recommendation",
    "nav.welcome":     "Welcome,",
    "nav.profile":     "Profile",
    "nav.logout":      "Logout",
    "nav.login":       "Login",
    "nav.register":    "Register",
    "nav.lang_btn":    "தமிழ்",

    /* ── Index ── */
    "index.title":     "Crop Recommendation System",
    "index.subtitle":  "Get personalized crop recommendations based on soil and climate parameters",
    "index.simple":    "Simple Predictor",
    "index.advanced":  "Advanced Soil Analysis",
    "index.card_title":"Enter Soil & Climate Details",
    "index.how_title": "How to Use",
    "index.how_body":  "Fill in the soil nutrients (N, P, K), temperature, humidity, pH level, and expected rainfall. Our AI model will recommend the best crop for your conditions.",
    "index.nutrients": "Soil Nutrients (ppm)",
    "index.climate":   "Climate & Environment",
    "index.location":  "Location / Weather",
    "index.nitrogen":  "Nitrogen (N) - Color Level",
    "index.phosphorus":"Phosphorus (P) - Color Level",
    "index.potassium": "Potassium (K) - Color Level",
    "index.sel_n":     "Select Nitrogen level",
    "index.sel_p":     "Select Phosphorus level",
    "index.sel_k":     "Select Potassium level",
    "index.red_low":   "Red (Low)",
    "index.yel_mid":   "Yellow (Medium)",
    "index.grn_high":  "Green (High)",
    "index.temp":      "Temperature",
    "index.temp_hint": "Celsius (°C). Leave blank to auto-fill from weather.",
    "index.humidity":  "Humidity",
    "index.hum_hint":  "Percentage (%). Leave blank to auto-fill from weather.",
    "index.ph":        "Soil pH",
    "index.ph_hint":   "pH Scale (0–14)",
    "index.rainfall":  "Rainfall",
    "index.rain_hint": "Millimeters (mm). Optional; auto-filled from weather if blank.",
    "index.city":      "City (optional)",
    "index.city_hint": "Provide a city to allow the app to autofill temperature & humidity from weather data.",
    "index.autofill":  "Autofill options",
    "index.autofill_hint": "If Temperature or Humidity are left blank, they'll be fetched from the weather API for the provided city.",
    "index.submit":    "Get Crop Recommendation",

    /* ── Result ── */
    "result.title":    "Recommended Crop",
    "result.desc":     "Based on the soil and climate parameters you provided, this is the best crop recommendation for your farming conditions.",
    "result.conf":     "Recommendation Confidence",
    "result.optimal":  "Optimal Match",
    "result.recommended": "Recommended",
    "result.weather_src":  "Weather Source",
    "result.weather_body": "Temperature/Humidity were auto-filled from weather data.",
    "result.disease":  "Possible Disease",
    "result.disease_label": "Disease:",
    "result.solution_label": "Solution:",
    "result.market":   "Market Data",
    "result.market_lbl": "Market:",
    "result.price_lbl":  "Price:",
    "result.suitable": "Suitable Options",
    "result.try_again":  "Try Again",
    "result.my_profile": "My Profile",
    "result.login_save": "Login to Save",
    "result.note":     "To get another recommendation, fill in different parameters and try again.",

    /* ── Login ── */
    "login.title":     "Login",
    "login.username":  "Username",
    "login.password":  "Password",
    "login.username_ph": "Enter your username",
    "login.password_ph": "Enter your password",
    "login.btn":       "Login",
    "login.no_account":"Don't have an account?",
    "login.register_link": "Register here",

    /* ── Register ── */
    "register.title":  "Create Account",
    "register.username": "Username",
    "register.email":  "Email",
    "register.password": "Password",
    "register.confirm":  "Confirm Password",
    "register.username_ph": "Enter your username",
    "register.email_ph":    "Enter your email",
    "register.password_ph": "Create password",
    "register.confirm_ph":  "Confirm password",
    "register.btn":    "Create Account",
    "register.have_account": "Already have an account?",
    "register.login_link":   "Login",
    "register.back":   "Back to Home",

    /* ── Profile ── */
    "profile.manage":  "Manage your account",
    "profile.username_lbl": "Username",
    "profile.email_lbl":    "Email",
    "profile.joined":  "Member Since",
    "profile.back":    "Back to Home",
    "profile.logout":  "Logout",
  },

  ta: {
    /* ── Navbar ── */
    "nav.brand":       "AI பயிர் பரிந்துரை",
    "nav.welcome":     "வரவேற்கிறோம்,",
    "nav.profile":     "சுயவிவரம்",
    "nav.logout":      "வெளியேறு",
    "nav.login":       "உள்நுழை",
    "nav.register":    "பதிவு செய்",
    "nav.lang_btn":    "English",

    /* ── Index ── */
    "index.title":     "பயிர் பரிந்துரை அமைப்பு",
    "index.subtitle":  "மண் மற்றும் காலநிலை அளவுருக்களின் அடிப்படையில் பரிந்துரைகளைப் பெறுங்கள்",
    "index.simple":    "எளிய கணிப்பு",
    "index.advanced":  "மேம்பட்ட மண் பகுப்பாய்வு",
    "index.card_title":"மண் மற்றும் காலநிலை விவரங்களை உள்ளிடுக",
    "index.how_title": "எப்படி பயன்படுத்துவது",
    "index.how_body":  "மண் ஊட்டச்சத்துக்கள் (N, P, K), வெப்பநிலை, ஈரப்பதம், pH அளவு மற்றும் மழையளவை நிரப்பவும். எங்கள் AI மாதிரி உங்கள் நிலைமைகளுக்கு சிறந்த பயிரை பரிந்துரைக்கும்.",
    "index.nutrients": "மண் ஊட்டச்சத்துக்கள் (ppm)",
    "index.climate":   "காலநிலை மற்றும் சூழல்",
    "index.location":  "இடம் / வானிலை",
    "index.nitrogen":  "நைட்ரஜன் (N) - நிற அளவு",
    "index.phosphorus":"பாஸ்பரஸ் (P) - நிற அளவு",
    "index.potassium": "பொட்டாசியம் (K) - நிற அளவு",
    "index.sel_n":     "நைட்ரஜன் அளவைத் தேர்ந்தெடுக்கவும்",
    "index.sel_p":     "பாஸ்பரஸ் அளவைத் தேர்ந்தெடுக்கவும்",
    "index.sel_k":     "பொட்டாசியம் அளவைத் தேர்ந்தெடுக்கவும்",
    "index.red_low":   "சிவப்பு (குறைவு)",
    "index.yel_mid":   "மஞ்சள் (நடுத்தரம்)",
    "index.grn_high":  "பச்சை (அதிகம்)",
    "index.temp":      "வெப்பநிலை",
    "index.temp_hint": "செல்சியஸ் (°C). வானிலையில் இருந்து தானாக நிரப்ப காலியாக விடவும்.",
    "index.humidity":  "ஈரப்பதம்",
    "index.hum_hint":  "சதவீதம் (%). வானிலையில் இருந்து தானாக நிரப்ப காலியாக விடவும்.",
    "index.ph":        "மண் pH",
    "index.ph_hint":   "pH அளவு (0–14)",
    "index.rainfall":  "மழையளவு",
    "index.rain_hint": "மில்லிமீட்டர் (mm). ஐச்சிக; காலியாக விட்டால் வானிலையில் இருந்து நிரப்பப்படும்.",
    "index.city":      "நகரம் (விருப்பத்தேர்வு)",
    "index.city_hint": "வெப்பநிலை மற்றும் ஈரப்பதத்தை தானாக நிரப்ப நகரத்தை வழங்கவும்.",
    "index.autofill":  "தானியங்கு நிரப்பு விருப்பங்கள்",
    "index.autofill_hint": "வெப்பநிலை அல்லது ஈரப்பதம் காலியாக இருந்தால், வழங்கப்பட்ட நகரத்திற்கான வானிலை API இல் இருந்து பெறப்படும்.",
    "index.submit":    "பயிர் பரிந்துரையைப் பெறு",

    /* ── Result ── */
    "result.title":    "பரிந்துரைக்கப்பட்ட பயிர்",
    "result.desc":     "நீங்கள் வழங்கிய மண் மற்றும் காலநிலை அளவுருக்களின் அடிப்படையில், இது உங்கள் விவசாய நிலைமைகளுக்கு சிறந்த பயிர் பரிந்துரை.",
    "result.conf":     "பரிந்துரை நம்பகத்தன்மை",
    "result.optimal":  "சிறந்த பொருத்தம்",
    "result.recommended": "பரிந்துரைக்கப்பட்டது",
    "result.weather_src":  "வானிலை ஆதாரம்",
    "result.weather_body": "வெப்பநிலை/ஈரப்பதம் வானிலை தரவிலிருந்து தானாக நிரப்பப்பட்டது.",
    "result.disease":  "சாத்தியமான நோய்",
    "result.disease_label": "நோய்:",
    "result.solution_label": "தீர்வு:",
    "result.market":   "சந்தை தரவு",
    "result.market_lbl": "சந்தை:",
    "result.price_lbl":  "விலை:",
    "result.suitable": "பொருத்தமான விருப்பங்கள்",
    "result.try_again":  "மீண்டும் முயற்சி",
    "result.my_profile": "என் சுயவிவரம்",
    "result.login_save": "சேமிக்க உள்நுழையவும்",
    "result.note":     "மற்றொரு பரிந்துரையைப் பெற, வேறு அளவுருக்களை நிரப்பி மீண்டும் முயற்சிக்கவும்.",

    /* ── Login ── */
    "login.title":     "உள்நுழை",
    "login.username":  "பயனர்பெயர்",
    "login.password":  "கடவுச்சொல்",
    "login.username_ph": "உங்கள் பயனர்பெயரை உள்ளிடவும்",
    "login.password_ph": "உங்கள் கடவுச்சொல்லை உள்ளிடவும்",
    "login.btn":       "உள்நுழை",
    "login.no_account":"கணக்கு இல்லையா?",
    "login.register_link": "இங்கே பதிவு செய்க",

    /* ── Register ── */
    "register.title":  "கணக்கை உருவாக்கு",
    "register.username": "பயனர்பெயர்",
    "register.email":  "மின்னஞ்சல்",
    "register.password": "கடவுச்சொல்",
    "register.confirm":  "கடவுச்சொல்லை உறுதிப்படுத்தவும்",
    "register.username_ph": "உங்கள் பயனர்பெயரை உள்ளிடவும்",
    "register.email_ph":    "உங்கள் மின்னஞ்சலை உள்ளிடவும்",
    "register.password_ph": "கடவுச்சொல்லை உருவாக்கவும்",
    "register.confirm_ph":  "கடவுச்சொல்லை உறுதிப்படுத்தவும்",
    "register.btn":    "கணக்கை உருவாக்கு",
    "register.have_account": "ஏற்கனவே கணக்கு உள்ளதா?",
    "register.login_link":   "உள்நுழை",
    "register.back":   "முகப்புக்கு திரும்பு",

    /* ── Profile ── */
    "profile.manage":  "உங்கள் கணக்கை நிர்வகிக்கவும்",
    "profile.username_lbl": "பயனர்பெயர்",
    "profile.email_lbl":    "மின்னஞ்சல்",
    "profile.joined":  "உறுப்பினர் தொடங்கி",
    "profile.back":    "முகப்புக்கு திரும்பு",
    "profile.logout":  "வெளியேறு",
  }
};

const RESULT_TAMIL_MAP = {
  crops: {
    apple: "ஆப்பிள்",
    banana: "வாழை",
    blackgram: "உளுந்து",
    chickpea: "கொண்டைக்கடலை",
    coconut: "தேங்காய்",
    coffee: "காப்பி",
    cotton: "பருத்தி",
    grapes: "திராட்சை",
    jute: "சணல்",
    kidneybeans: "மொச்சைக் காராமணி",
    lentil: "மசூர் பருப்பு",
    maize: "மக்காச்சோளம்",
    mango: "மாம்பழம்",
    mothbeans: "மொத் பீன்ஸ்",
    mungbean: "பாசிப்பயறு",
    muskmelon: "முலாம்பழம்",
    orange: "ஆரஞ்சு",
    papaya: "பப்பாளி",
    pigeonpeas: "துவரம் பருப்பு",
    pomegranate: "மாதுளை",
    pulses: "பருப்பு வகைகள்",
    rice: "நெல்",
    watermelon: "தர்பூசணி"
  },
  diseases: {
    blight: "இலைக்கருகல் நோய்",
    leafspot: "இலைப் புள்ளி நோய்",
    rust: "துரு நோய்",
    wilt: "வாடல் நோய்",
    mildew: "பூஞ்சைத் தூள் நோய்",
    smut: "ஸ்மட் நோய்",
    blast: "பிளாஸ்ட் நோய்",
    rot: "அழுகல் நோய்"
  },
  solutions: {
    "treat seeds with biofungicide, improve field drainage, and avoid continuous pulse cultivation in same plot.":
      "விதைகளை உயிர் பூஞ்சைநாசினியால் சிகிச்சை செய்யவும், வயலில் நீர்வடிகாலை மேம்படுத்தவும், அதே நிலத்தில் தொடர்ந்து பருப்பு பயிரிடுவதைத் தவிர்க்கவும்.",
    "spray recommended fungicide, remove infected plant parts, and avoid overhead irrigation during humid periods.":
      "பரிந்துரைக்கப்பட்ட பூஞ்சைநாசினியை தெளிக்கவும், பாதிக்கப்பட்ட தாவரப் பகுதிகளை அகற்றவும், ஈரமான காலங்களில் மேலிருந்து நீர்ப்பாய்ச்சுவதைத் தவிர்க்கவும்.",
    "ensure proper spacing, use disease-free seeds, and apply organic fungicides as preventive measure.":
      "சரியான இடைவெளியைப் பின்பற்றவும், நோயில்லா விதைகளைப் பயன்படுத்தவும், தடுப்பு முறையாக உயிர் பூஞ்சைநாசினிகளைப் பயன்படுத்தவும்.",
    "practice crop rotation, improve soil health with compost, and apply suitable bio-control agents.":
      "பயிர் சுழற்சியைப் பின்பற்றவும், உரமண்/கம்போஸ்ட் மூலம் மண் ஆரோக்கியத்தை மேம்படுத்தவும், பொருத்தமான உயிரியல் கட்டுப்பாட்டு முகவர்களைப் பயன்படுத்தவும்.",
    "remove infected residue, rotate crops, and spray mancozeb at recommended dose.":
      "பாதிக்கப்பட்ட பயிர் எச்சங்களை அகற்றவும், பயிர் சுழற்சியைப் பின்பற்றவும், பரிந்துரைக்கப்பட்ட அளவில் மான்கோசெப் தெளிக்கவும்."
  }
};

/* ─────────────────────────────────────────────
   Core engine
───────────────────────────────────────────── */
(function () {
  const STORAGE_KEY = "crop_lang";
  const DEFAULT_LANG = "en";

  function currentLang() {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
  }

  function t(key) {
    const lang = currentLang();
    return (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) ||
           (TRANSLATIONS[DEFAULT_LANG] && TRANSLATIONS[DEFAULT_LANG][key]) ||
           key;
  }

  function normalizeKey(text) {
    return (text || "")
      .toString()
      .toLowerCase()
      .replace(/[\-_]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function translateCropToTamil(cropName) {
    const normalized = normalizeKey(cropName);
    const compact = normalized.replace(/\s+/g, "");
    return RESULT_TAMIL_MAP.crops[compact] || RESULT_TAMIL_MAP.crops[normalized] || cropName;
  }

  function translateDiseaseToTamil(diseaseName) {
    const normalized = normalizeKey(diseaseName);
    for (const key in RESULT_TAMIL_MAP.diseases) {
      if (normalized.includes(key)) {
        return RESULT_TAMIL_MAP.diseases[key];
      }
    }
    return diseaseName;
  }

  function translateSolutionToTamil(solutionText) {
    const normalized = normalizeKey(solutionText);
    if (RESULT_TAMIL_MAP.solutions[normalized]) {
      return RESULT_TAMIL_MAP.solutions[normalized];
    }

    // Keyword-based fallback for unseen but similar advisory sentences.
    if (normalized.includes("remove infected residue") && normalized.includes("rotate crops")) {
      return "பாதிக்கப்பட்ட பயிர் எச்சங்களை அகற்றவும், பயிர் சுழற்சியைப் பின்பற்றவும், பொருத்தமான பூஞ்சைநாசினியை பரிந்துரைக்கப்பட்ட அளவில் தெளிக்கவும்.";
    }
    if (normalized.includes("mancozeb")) {
      return "மான்கோசெப்பை பரிந்துரைக்கப்பட்ட அளவில் தெளிக்கவும்.";
    }

    return solutionText;
  }

  function applyResultDynamicTranslations(lang) {
    const cropEl = document.querySelector(".crop-name[data-i18n-dynamic='crop']");
    if (cropEl) {
      if (!cropEl.dataset.enValue) cropEl.dataset.enValue = cropEl.textContent.trim();
      cropEl.textContent = lang === "ta"
        ? translateCropToTamil(cropEl.dataset.enValue)
        : cropEl.dataset.enValue;
    }

    const suggestionEl = document.querySelector(".crop-suggestions-text[data-i18n-dynamic='suggestions']");
    if (suggestionEl) {
      if (!suggestionEl.dataset.enValue) suggestionEl.dataset.enValue = suggestionEl.textContent.trim();
      if (lang === "ta") {
        suggestionEl.textContent = suggestionEl.dataset.enValue
          .split(",")
          .map(function (item) { return translateCropToTamil(item.trim()); })
          .join(", ");
      } else {
        suggestionEl.textContent = suggestionEl.dataset.enValue;
      }
    }

    const diseaseEl = document.querySelector(".disease-name-text[data-i18n-dynamic='disease']");
    if (diseaseEl) {
      if (!diseaseEl.dataset.enValue) diseaseEl.dataset.enValue = diseaseEl.textContent.trim();
      diseaseEl.textContent = lang === "ta"
        ? translateDiseaseToTamil(diseaseEl.dataset.enValue)
        : diseaseEl.dataset.enValue;
    }

    const solutionEl = document.querySelector(".disease-solution-text[data-i18n-dynamic='solution']");
    if (solutionEl) {
      if (!solutionEl.dataset.enValue) solutionEl.dataset.enValue = solutionEl.textContent.trim();
      solutionEl.textContent = lang === "ta"
        ? translateSolutionToTamil(solutionEl.dataset.enValue)
        : solutionEl.dataset.enValue;
    }

    const confidenceEl = document.querySelector(".confidence-text[data-confidence]");
    if (confidenceEl) {
      const value = confidenceEl.getAttribute("data-confidence") || "";
      confidenceEl.textContent = lang === "ta"
        ? value + "% நம்பகத்தன்மை"
        : value + "% Confidence";
    }
  }

  function applyTranslations() {
    const lang = currentLang();
    document.documentElement.lang = lang === "ta" ? "ta" : "en";

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      const key = el.getAttribute("data-i18n");
      const val = t(key);
      if (!val) return;

      /* placeholder inputs */
      if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
        el.placeholder = val;
      /* option elements */
      } else if (el.tagName === "OPTION") {
        el.textContent = val;
      /* elements that contain an <i> icon — preserve it */
      } else {
        const icon = el.querySelector("i");
        if (icon) {
          el.innerHTML = "";
          el.appendChild(icon.cloneNode(true));
          el.appendChild(document.createTextNode(" " + val));
        } else {
          el.textContent = val;
        }
      }
    });

    /* update toggle button label */
    document.querySelectorAll(".lang-toggle-btn").forEach(function (btn) {
      btn.textContent = lang === "ta" ? "English" : "தமிழ்";
      btn.title = lang === "ta" ? "Switch to English" : "தமிழில் மாற்று";
    });

    applyResultDynamicTranslations(lang);
  }

  function toggleLang() {
    const next = currentLang() === "en" ? "ta" : "en";
    localStorage.setItem(STORAGE_KEY, next);
    applyTranslations();
  }

  /* Run on DOM ready */
  document.addEventListener("DOMContentLoaded", function () {
    applyTranslations();
  });

  /* Expose globally so inline onclick can also call it */
  window.i18nToggle = toggleLang;
  window.i18nApply = applyTranslations;
})();
