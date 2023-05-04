/* eslint-disable vue/multi-word-component-names */
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "animate.css";

Vue.config.productionTip = false;

// for later versions of primevue
import PrimeVue from "primevue/config";
Vue.use(PrimeVue, {
  ripple: true,
  locale: {
    firstDayOfWeek: 1,
    dayNames: [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ],
    dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
    monthNames: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
    monthNamesShort: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    today: "Today",
    clear: "Clear",
    dateFormat: "mm/dd/yy",
    weekHeader: "Wk",
  },
});
//Vue.prototype.$primevue = { ripple: true };

import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Toast from "primevue/toast";
import ToastService from "primevue/toastservice";
// import Card from "primevue/card";
import Dropdown from "primevue/dropdown";
import InputSwitch from "primevue/inputswitch";
import InputNumber from "primevue/inputnumber";
//import DataTable from "primevue/datatable";
//import Column from "primevue/column";
//import Panel from "primevue/panel";
import Toolbar from "primevue/toolbar";
import ProgressSpinner from "primevue/progressspinner";
import ProgressBar from "primevue/progressbar";
import Calendar from "primevue/calendar";
//import Checkbox from "primevue/checkbox";
import Autocomplete from "primevue/autocomplete";
import Tooltip from "primevue/tooltip";
//import ToggleButton from "primevue/togglebutton";
import Message from "primevue/message";
import InlineMessage from "primevue/inlinemessage";
//import SelectButton from "primevue/selectbutton";
import Menu from "primevue/menu";
import Dialog from "primevue/dialog";
import Textarea from "primevue/textarea";
import Skeleton from "primevue/skeleton";
import BlockUI from "primevue/blockui";
import Tag from "primevue/tag";
import RadioButton from "primevue/radiobutton";
import SelectButton from "primevue/selectbutton";

//import "primevue/resources/themes/saga-blue/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

import "primeflex/primeflex.css";

const app = new Vue({
  router,
  store,
  render: (h) => h(App),
});

Vue.use(ToastService);

Vue.component("InputText", InputText);
Vue.component("Button", Button);
Vue.component("Toast", Toast);
// Vue.component("Card", Card);
Vue.component("Dropdown", Dropdown);
Vue.component("InputText", InputText);
Vue.component("InputSwitch", InputSwitch);
Vue.component("InputNumber", InputNumber);
//Vue.component("DataTable", DataTable);
//Vue.component("Column", Column);
//Vue.component("Panel", Panel);
Vue.component("Toolbar", Toolbar);
Vue.component("ProgressSpinner", ProgressSpinner);
Vue.component("ProgressBar", ProgressBar);
Vue.component("Calendar", Calendar);
//Vue.component("Checkbox", Checkbox);
Vue.component("AutoComplete", Autocomplete);
Vue.directive("tooltip", Tooltip);
//Vue.component("ToggleButton", ToggleButton);
Vue.component("Message", Message);
Vue.component("InlineMessage", InlineMessage);
//Vue.component("SelectButton", SelectButton);
Vue.component("Menu", Menu);
Vue.component("Dialog", Dialog);
Vue.component("Textarea", Textarea);
Vue.component("Skeleton", Skeleton);
Vue.component("BlockUI", BlockUI);
Vue.component("Tag", Tag);
Vue.component("RadioButton", RadioButton);
Vue.component("SelectButton", SelectButton);

app.$mount("#app");
