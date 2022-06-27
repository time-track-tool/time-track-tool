<template>
  <div id="layout-config" :class="containerClass">
    <a
      href="#"
      class="layout-config-button"
      id="layout-config-button"
      @click="toggleConfigurator"
    >
      <i class="pi pi-cog"></i>
    </a>
    <Button
      class="p-button-danger layout-config-close p-button-rounded p-button-text"
      icon="pi pi-times"
      @click="hideConfigurator"
      :style="{ 'z-index': 1 }"
    ></Button>

    <div class="layout-config-content">
      <h5>Themes</h5>
      <h6 class="mt-0">Bootstrap</h6>
      <div class="grid free-themes">
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'bootstrap4-light-blue')"
          >
            <img
              :src="publicPath + 'images/themes/bootstrap4-light-blue.svg'"
              alt="Bootstrap Light Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'bootstrap4-light-purple')"
          >
            <img
              :src="publicPath + 'images/themes/bootstrap4-light-purple.svg'"
              alt="Bootstrap Light Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'bootstrap4-dark-blue', true)"
          >
            <img
              :src="publicPath + 'images/themes/bootstrap4-dark-blue.svg'"
              alt="Bootstrap Dark Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'bootstrap4-dark-purple', true)"
          >
            <img
              :src="publicPath + 'images/themes/bootstrap4-dark-purple.svg'"
              alt="Bootstrap Dark Blue"
            />
          </button>
        </div>
      </div>

      <h6>Tailwind</h6>
      <div class="grid free-themes">
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'tailwind-light')"
          >
            <img
              :src="publicPath + 'images/themes/tailwind-light.png'"
              alt="Tailwind Light"
            />
          </button>
        </div>
      </div>

      <h6>Fluent UI</h6>
      <div class="grid free-themes">
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'fluent-light')"
          >
            <img
              :src="publicPath + 'images/themes/fluent-light.png'"
              alt="Fluent Light"
            />
          </button>
        </div>
      </div>

      <h6>PrimeOne Design 2021</h6>
      <div class="grid free-themes">
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'saga-blue')"
          >
            <img
              :src="publicPath + 'images/themes/saga-blue.png'"
              alt="Saga Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'saga-green')"
          >
            <img
              :src="publicPath + 'images/themes/saga-green.png'"
              alt="Saga Green"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'saga-orange')"
          >
            <img
              :src="publicPath + 'images/themes/saga-orange.png'"
              alt="Saga Orange"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'saga-purple')"
          >
            <img
              :src="publicPath + 'images/themes/saga-purple.png'"
              alt="Saga Purple"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'vela-blue', true)"
          >
            <img
              :src="publicPath + 'images/themes/vela-blue.png'"
              alt="Vela Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'vela-green', true)"
          >
            <img
              :src="publicPath + 'images/themes/vela-green.png'"
              alt="Vela Green"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'vela-orange', true)"
          >
            <img
              :src="publicPath + 'images/themes/vela-orange.png'"
              alt="Vela Orange"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'vela-purple', true)"
          >
            <img
              :src="publicPath + 'images/themes/vela-purple.png'"
              alt="Vela Purple"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'arya-blue', true)"
          >
            <img
              :src="publicPath + 'images/themes/arya-blue.png'"
              alt="Arya Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'arya-green', true)"
          >
            <img
              :src="publicPath + 'images/themes/arya-green.png'"
              alt="Arya Green"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'arya-orange', true)"
          >
            <img
              :src="publicPath + 'images/themes/arya-orange.png'"
              alt="Arya Orange"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'arya-purple', true)"
          >
            <img
              :src="publicPath + 'images/themes/arya-purple.png'"
              alt="Arya Purple"
            />
          </button>
        </div>
      </div>

      <h6>
        PrimeOne Design 2022 -<Tag
          class="ml-2"
          value="NEW"
          rounded
          severity="success"
        ></Tag>
      </h6>
      <div class="grid free-themes">
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-light-indigo')"
          >
            <img
              :src="publicPath + 'images/themes/lara-light-indigo.png'"
              alt="Lara Light Indigo"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-light-blue')"
          >
            <img
              :src="publicPath + 'images/themes/lara-light-blue.png'"
              alt="Lara Light Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-light-purple')"
          >
            <img
              :src="publicPath + 'images/themes/lara-light-purple.png'"
              alt="Lara Light Purple"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-light-teal')"
          >
            <img
              :src="publicPath + 'images/themes/lara-light-teal.png'"
              alt="Lara Light Teal"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-dark-indigo', true)"
          >
            <img
              :src="publicPath + 'images/themes/lara-dark-indigo.png'"
              alt="Lara Dark Indigo"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-dark-blue', true)"
          >
            <img
              :src="publicPath + 'images/themes/lara-dark-blue.png'"
              alt="Lara Dark Blue"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-dark-purple', true)"
          >
            <img
              :src="publicPath + 'images/themes/lara-dark-purple.png'"
              alt="Lara Dark Purple"
            />
          </button>
        </div>
        <div class="col-3 text-center">
          <button
            class="p-link"
            type="button"
            @click="changeTheme($event, 'lara-dark-teal', true)"
          >
            <img
              :src="publicPath + 'images/themes/lara-dark-teal.png'"
              alt="Lara Dark Teal"
            />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    layoutMode: {
      type: String,
      default: null,
    },
    layoutColorMode: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      theme: "vela-blue",
      darkTheme: false,
      active: false,
      d_layoutMode: this.layoutMode,
      d_layoutColorMode: this.layoutColorMode,
      scale: 16,
      scales: [12, 13, 14, 15, 16],
      publicPath: process.env.BASE_URL,
    };
  },
  watch: {
    $route() {
      if (this.active) {
        this.active = false;
        this.unbindOutsideClickListener();
      }
    },
    layoutMode(newValue) {
      this.d_layoutMode = newValue;
    },
    layoutColorMode(newValue) {
      this.d_layoutColorMode = newValue;
    },
  },
  outsideClickListener: null,
  methods: {
    toggleConfigurator(event) {
      this.active = !this.active;
      event.preventDefault();

      if (this.active) this.bindOutsideClickListener();
      else this.unbindOutsideClickListener();
    },
    hideConfigurator(event) {
      this.active = false;
      this.unbindOutsideClickListener();
      event.preventDefault();
    },
    changeInputStyle(value) {
      this.$primevue.config.inputStyle = value;
    },
    changeRipple(value) {
      this.$primevue.config.ripple = value;
    },
    changeLayoutColor(event, layoutColor) {
      this.$emit("layout-color-change", layoutColor);
      event.preventDefault();
    },
    bindOutsideClickListener() {
      if (!this.outsideClickListener) {
        this.outsideClickListener = (event) => {
          if (this.active && this.isOutsideClicked(event)) {
            this.active = false;
          }
        };
        document.addEventListener("click", this.outsideClickListener);
      }
    },
    unbindOutsideClickListener() {
      if (this.outsideClickListener) {
        document.removeEventListener("click", this.outsideClickListener);
        this.outsideClickListener = null;
      }
    },
    isOutsideClicked(event) {
      return !(
        this.$el.isSameNode(event.target) || this.$el.contains(event.target)
      );
    },
    decrementScale() {
      this.scale--;
      this.applyScale();
    },
    incrementScale() {
      this.scale++;
      this.applyScale();
    },
    applyScale() {
      document.documentElement.style.fontSize = this.scale + "px";
    },
    changeTheme(event, theme, dark = false) {
      let themeElement = document.getElementById("theme-link");
      themeElement.setAttribute(
        "href",
        themeElement.getAttribute("href").replace(this.theme, theme)
      );
      this.theme = theme;
      this.darkTheme = dark;

      if (theme.startsWith("md")) {
        this.$primevue.config.ripple = true;
      }
    },
  },
  computed: {
    containerClass() {
      return ["layout-config", { "layout-config-active": this.active }];
    },
    rippleActive() {
      return this.$primevue.config.ripple;
    },
    inputStyle() {
      return this.$appState.inputStyle;
    },
  },
};
</script>

<style>
.layout-config .free-themes img {
  width: 2rem;
  border-radius: 4px;
  transition: transform 0.2s;
}
.layout-config .layout-config-content {
  position: relative;
  overflow: auto;
  height: 100vh;
  padding: 2rem;
}
.layout-config {
  position: fixed;
  top: 0;
  padding: 0;
  right: 0;
  width: 20rem;
  z-index: 999;
  height: 100vh;
  transform: translateX(100%);
  transition: transform 0.2s;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.02), 0 0 2px rgba(0, 0, 0, 0.05),
    0 1px 4px rgba(0, 0, 0, 0.08) !important;
  color: var(--text-color);
  background-color: var(--surface-overlay);
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
}
.layout-config.layout-config-active {
  transform: translateX(0);
}
.layout-config .layout-config-button {
  display: block;
  position: absolute;
  width: 24px;
  height: 24px;
  line-height: 24px;
  background-color: var(--primary-color);
  color: var(--primary-color-text);
  text-align: center;
  top: 0px;
  left: -24px;
  z-index: -1;
  overflow: hidden;
  cursor: pointer;
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
  transition: background-color 0.2s;
}
.layout-config .config-scale {
  display: flex;
  align-items: center;
  margin: 1rem 0 2rem 0;
}
.field-checkbox,
.field-radiobutton {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  margin-right: -0.5rem;
  margin-left: -0.5rem;
  margin-top: -0.5rem;
}
.text-center {
  text-align: center !important;
}
.col-3 {
  width: 25%;
}
.col-2,
.col-3 {
  flex: 0 0 auto;
  padding: 0.5rem;
}
.block {
  display: block !important;
}
.layout-config .config-scale i.scale-active {
  font-size: 1.25rem;
  color: var(--primary-color);
}
.layout-config .config-scale i {
  margin-right: 0.5rem;
  font-size: 0.75rem;
  color: var(--text-color-secondary);
}
.layout-config .layout-config-close {
  position: absolute;
  right: 1rem;
  top: 1rem;
  z-index: 1;
}
.mt-0 {
  margin-top: 0 !important;
}
h5 {
  font-size: 1.25rem;
}
h1,
h2,
h3,
h4,
h5,
h6 {
  margin: 1.5rem 0 1rem 0;
  font-family: inherit;
  font-weight: 500;
  line-height: 1.2;
  color: inherit;
}
</style>
