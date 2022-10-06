<template>
  <div id="app">
    <div
      class="border-b p-d-flex p-p-3 p-jc-between"
      v-if="theme_set === true && this.new_tt_iface === true"
    >
      <Button
        type="button"
        label="Back to Roundup issue tracker"
        icon="pi pi-angle-left"
        class="p-button-secondary"
        @click="goto_tracker"
      />
      <div></div>
      <div class="p-ml-auto">
        <SelectButton
          v-model="my_dark_mode"
          :options="dark_mode_options"
          dataKey="value"
          optionValue="value"
        >
          <template #option="slotProps">
            <i :class="slotProps.option.icon"></i>
          </template>
        </SelectButton>
        <Button
          v-if="dev"
          class="p-mr-2 p-ml-2"
          :class="debug ? 'p-button-success' : ''"
          label="Toggle Debug"
          @click="setDebug(!debug)"
        />
        <Button
          v-if="dev"
          class="p-mr-2"
          :class="$route.params.user_id == '9' ? 'p-button-success' : ''"
          label="9"
          @click="switch_user(9)"
        />
        <Button
          v-if="dev"
          class="p-mr-2"
          :class="$route.params.user_id == '1528' ? 'p-button-success' : ''"
          label="1528"
          @click="switch_user(1528)"
        />
        <Button
          v-if="dev"
          label="2300"
          :class="$route.params.user_id == '2300' ? 'p-button-success' : ''"
          @click="switch_user(2300)"
        />
      </div>
    </div>
    <!-- <AppConfig />
    <transition name="layout-mask">
      <div
        class="layout-mask p-component-overlay"
        v-if="mobileMenuActive"
      ></div>
    </transition> -->
    <router-view />
  </div>
</template>

<script>
import { format } from "date-fns";
import { mapActions, mapMutations, mapState, mapGetters } from "vuex";
import qs from "qs";
// import AppConfig from "./AppConfig.vue";

export default {
  name: "App",
  data: () => {
    return {
      mobileMenuActive: false,
      users: {
        9: { name: "benesch@ds1.internal", pw: "a" },
        2300: { name: "caban@ds1.internal", pw: "a" },
        1528: { name: "georgiev@ds1.internal", pw: "a" },
      },
      dev: process.env.NODE_ENV === "development",
      my_dark_mode: null,
      theme_set: false,
      dark_mode_options: [
        { icon: "pi pi-sun", value: false },
        { icon: "pi pi-moon", value: true },
      ],
    };
  },
  components: {
    // AppConfig,
  },
  watch: {
    my_dark_mode: function () {
      if (this.my_dark_mode !== this.dark_mode) {
        this.set_dark_mode({
          params: { user_id: this.user_id },
          data: {
            dark_mode: this.my_dark_mode === true ? 1 : 0,
            "@etag": this.user_etag,
          },
        }).then(() =>
          this.get_dark_mode({ params: { user_id: this.user_id } })
        );
      }
      if (this.my_dark_mode === true) {
        this.changeTheme("bootstrap4-dark-blue");
      } else {
        this.changeTheme("bootstrap4-light-blue");
      }
      this.theme_set = true;
    },
  },
  computed: {
    ...mapState("rest", [
      "logged_in",
      "pending",
      "error",
      "user_dynamic",
      "dark_mode",
      "new_tt_iface",
      "user_etag",
    ]),
    ...mapGetters(["debug", "user_id"]),
  },
  methods: {
    ...mapActions("rest", [
      "login",
      "logout",
      "get_new_tt_iface",
      "get_dark_mode",
      "set_dark_mode",
    ]),
    ...mapMutations(["setUserId", "setDebug"]),
    changeTheme(theme) {
      let themeElement = document.getElementById("theme-link");
      let old_uri = themeElement.getAttribute("href");
      let new_uri = old_uri.replace(
        /(.*?\/themes\/)(.*?)(\/theme.css)/,
        "$1" + theme + "$3"
      );
      console.log(old_uri, new_uri);
      themeElement.setAttribute("href", new_uri);
      if (theme.startsWith("md")) {
        this.$primevue.config.ripple = true;
      }
    },
    goto_tracker: function () {
      let x = window.location.href.split("#")[0].split("/");
      x.pop();
      window.location = x.join("/");
    },
    switch_user: function (user_id) {
      this.logout().then(() => {
        console.log(user_id);
        this.login({
          data: qs.stringify({
            __login_name: this.users[user_id].name,
            __login_password: this.users[user_id].pw,
            "@action": "Login",
          }),
        }).then(() => {
          console.log(user_id);
          this.setUserId(user_id);
          this.$router.push(
            "/" + user_id + "/week/2021/" + format(new Date(), "I")
          );
        });
      });
    },
  },
  created: function () {
    // for later versions of primevue
    // this.$primevue.config.locale.firstDayOfWeek = 1;
    this.get_new_tt_iface({
      params: { user_id: this.$route.params.user_id },
    }).then(() => {
      if (this.new_tt_iface === false) {
        this.goto_tracker();
      } else {
        this.get_dark_mode({
          params: { user_id: this.$route.params.user_id },
        }).then(() => {
          this.my_dark_mode = this.dark_mode;
        });
      }
    });
  },
};
</script>

<style>
.p-formgroup-inline {
  flex-wrap: nowrap !important;
}
.border {
  border: 1px solid var(--surface-d);
}
.border-tbl {
  border-top: 1px solid var(--surface-d);
  border-bottom: 1px solid var(--surface-d);
  border-left: 1px solid var(--surface-d);
}
.border-tbr {
  border-top: 1px solid var(--surface-d);
  border-bottom: 1px solid var(--surface-d);
  border-right: 1px solid var(--surface-d);
}
.border-tb {
  border-top: 1px solid var(--surface-d);
  border-bottom: 1px solid var(--surface-d);
}
.border-t {
  border-top: 1px solid var(--surface-d);
}
.border-b {
  border-bottom: 1px solid var(--surface-d);
}
.w8 {
  width: 8em;
}
.w5 {
  width: 5em;
}
.w3 {
  width: 3em;
}
.tc {
  text-align: center;
}
body,
html {
  font-size: 14px;
  margin: 0;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  background-color: var(--surface-a);
  font-family: var(--font-family);
  font-weight: 400;
  color: var(--text-color);
}

#app {
}
</style>
