<template>
  <div>
    <div
      class="border-tb p-d-flex p-jc-end p-ai-center p-highlight"
      :style="day_is_weekend ? 'background: var(--surface-border)' : ''"
      style="
        padding-top: 1rem;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
        height: 4.5rem;
      "
    >
      <div
        v-if="is_first && $route.params.range === 'month'"
        class="p-mr-2"
        style="padding-left: 1em"
      >
        <Button
          type="button"
          @click="toggle_menu"
          icon="pi pi-copy"
          class="p-button-text"
          disabled
        />
        <Menu
          class="p-button-success p-button-text t5-menu"
          :model="menu_items_first_dom"
          ref="menu"
          :popup="true"
        ></Menu>
      </div>
      <div
        v-else-if="is_first && $route.params.range === 'week'"
        class="p-mr-2"
        style="padding-left: 1em"
      >
        <Button
          type="button"
          @click="toggle_menu"
          icon="pi pi-copy"
          class="p-button-text"
          :disabled="!enabled"
        />
        <Menu
          class="p-button-success p-button-text t5-menu"
          :model="menu_items_first_dow"
          ref="menu"
          :popup="true"
        ></Menu>
      </div>
      <div
        v-else-if="$route.params.range === 'month'"
        class="p-mr-2"
        style="padding-left: 1em"
      >
        <Button
          type="button"
          @click="toggle_menu"
          icon="pi pi-copy"
          class="p-button-text"
          :disabled="!enabled"
        />
        <Menu
          class="p-button-success p-button-text t5-menu"
          :model="menu_items_view_month"
          ref="menu"
          :popup="true"
        ></Menu>
      </div>
      <div
        v-else-if="$route.params.range === 'week'"
        class="p-mr-2"
        style="padding-left: 1em"
      >
        <Button
          type="button"
          @click="toggle_menu"
          icon="pi pi-copy"
          class="p-button-text"
          :disabled="!enabled"
        />
        <Menu
          class="p-button-success p-button-text t5-menu"
          :model="menu_items_view_week"
          ref="menu"
          :popup="true"
        ></Menu>
      </div>
      <div v-else-if="is_first" class="p-mr-2" style="padding-left: 1em">
        <Button
          type="button"
          @click="toggle_menu"
          icon="pi pi-copy"
          class="p-button-text"
          disabled="disabled"
        />
        <Menu
          class="p-button-success p-button-text t5-menu"
          :model="[]"
          ref="menu"
          :popup="true"
        ></Menu>
      </div>
      <div v-else class="p-mr-2" style="padding-left: 1em">
        <Button
          type="button"
          @click="toggle_menu"
          class="p-button-text"
          :disabled="!enabled"
          icon="pi pi-copy"
        />
        <Menu
          class="p-button-success p-button-text t5-menu"
          :model="menu_items_day"
          ref="menu"
          :popup="true"
        ></Menu>
      </div>
      <div
        class="tc p-mr-2"
        :class="enabled ? '' : 'p-disabled'"
        style="white-space: nowrap; text-align: left"
      >
        {{ format_date(date, "ccc, PP") }}
      </div>
      <div
        class="tc p-mr-2"
        :class="enabled ? '' : 'p-disabled'"
        style="flex-grow: 1; text-align: right; font-weight: bold"
      >
        When did you work?
      </div>
      <div class="w5 tc p-mr-2" :class="enabled ? '' : 'p-disabled'">
        <Tag
          :id="'att_sum_' + daily_record.id"
          v-bind:class="{
            animate__animated: animate,
            animate__bounceIn: animate,
          }"
          :severity="
            sums_equal
              ? 'success'
              : att_sum === 0 && day_is_empty
              ? 'info'
              : 'danger'
          "
          >&Sigma; {{ att_sum }}h</Tag
        >
      </div>
    </div>
    <div>
      <TimeAtts
        v-for="(att_id, idx) in att_ids"
        v-bind:daily_record_id="daily_record.id"
        v-bind:att_id="att_id"
        v-bind:start_overlaps="start_overlaps[att_id]"
        v-bind:end_overlaps="end_overlaps[att_id]"
        v-bind:too_much="too_much[att_id]"
        v-bind:day_enabled="enabled && all_atts_loaded"
        v-bind:float_labels="idx === 0"
        v-bind:is_last="idx === att_ids.length - 1"
        :key="'att_' + att_id"
        @update="update_att"
        @delete="delete_att"
        @loaded="att_loaded"
        @created="att_created"
        @set_error="set_error"
        @clear_error="clear_error"
      />
    </div>
  </div>
</template>

<script>
import defines from "../defines";
import TimeAtts from "./TimeAtts.vue";
import {
  format,
  add,
  areIntervalsOverlapping,
  isAfter,
  isEqual,
} from "date-fns";
import { v4 as uuidv4 } from "uuid";
import { mapState } from "vuex";

export default {
  name: "DayLeft",
  props: {
    daily_record: { type: Object, required: true },
    is_first: { type: Boolean, required: true },
    sums_equal: { type: Boolean, required: true },
    update: { type: Boolean, required: true },
    enabled_from_above: { type: Boolean, required: true },
    day_is_empty: { type: Boolean, required: true },
    day_is_weekend: { type: Boolean, required: true },
  },
  data: function () {
    return {
      format_date: format,
      defs: defines,
      att_ids: [],
      loaded_att_ids: [],
      atts: {},
      att_errors: [],
      att_sum: 0,
      att_off_sum: 0,
      att_travel_sum: 0,
      start_overlaps: {},
      end_overlaps: {},
      too_much: {},
      animate: false,
      menu_items_first_dow: [
        {
          label: "Everything",
          items: [
            {
              label: "day to whole week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_week", {
                  copy_atts: true,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
            {
              label: "from last week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_week", {
                  copy_atts: true,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Attendance only",
          items: [
            {
              label: "day to whole week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_week", {
                  copy_atts: true,
                  copy_trs: false,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
            {
              label: "from last week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_week", {
                  copy_atts: true,
                  copy_trs: false,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Project Effort only",
          items: [
            {
              label: "day to whole week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_week", {
                  copy_atts: false,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
            {
              label: "from last week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_week", {
                  copy_atts: false,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
      ],
      menu_items_first_dom: [
        {
          label: "Everything",
          items: [
            {
              label: "day to whole month",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_month", {
                  copy_atts: true,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to month copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Attendance only",
          items: [
            {
              label: "day to whole month",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_month", {
                  copy_atts: true,
                  copy_trs: false,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to month copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Project Effort only",
          items: [
            {
              label: "day to whole month",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_month", {
                  copy_atts: false,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to month copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
      ],
      menu_items_view_week: [
        {
          label: "Everything",
          items: [
            {
              label: "day to whole week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_week", {
                  copy_atts: true,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: true,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Attendance only",
          items: [
            {
              label: "day to whole week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_week", {
                  copy_atts: true,
                  copy_trs: false,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: true,
                  copy_trs: false,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Project Effort only",
          items: [
            {
              label: "day to whole week",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_day_to_week", {
                  copy_atts: false,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Day to week copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: false,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
      ],
      menu_items_view_month: [
        {
          label: "Everything",
          items: [
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: true,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Attendance only",
          items: [
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: true,
                  copy_trs: false,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Project Effort only",
          items: [
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: false,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
      ],
      menu_items_day: [
        {
          label: "Everything",
          items: [
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: true,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Attendance only",
          items: [
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: true,
                  copy_trs: false,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
        {
          label: "Project Effort only",
          items: [
            {
              label: "from last day",
              icon: "pi pi-angle-right",
              command: () => {
                this.$emit("copy_from_last_day", {
                  copy_atts: false,
                  copy_trs: true,
                });
                this.$toast.add({
                  severity: "success",
                  summary: "Last day copied",
                  detail: "",
                  life: 3000,
                });
              },
            },
          ],
        },
      ],
    };
  },
  components: {
    TimeAtts,
  },
  watch: {
    att_sum: function () {
      this.animate = true;
      document
        .getElementById("att_sum_" + this.daily_record.id)
        .addEventListener(
          "animationend",
          () => {
            this.animate = false;
          },
          { once: true }
        );
    },
    update: function () {
      if (this.update === true) {
        console.log("i should update myself");
        this.update_me();
      } else {
        console.log("skip update");
      }
    },
    all_atts_loaded: function () {
      if (this.all_atts_loaded === true) {
        this.update_sum();
        this.verify_atts();
        if (this.atts_valid()) {
          this.$emit("valid", true);
          this.$emit("sumchanged", {
            on: this.att_sum,
            off: this.att_off_sum,
            travel: this.att_travel_sum,
            refetch_daily_record: false,
          });
        } else {
          this.$emit("valid", false);
        }
        // resort this.att_ids based on start time
      }
    },
    enabled: function () {
      if (this.enabled && !this.last_is_empty()) {
        this.att_ids.push(this.add_empty());
      } else if (
        !this.enabled &&
        (this.last_is_empty() || this.last_is_incomplete())
      ) {
        this.delete_att(this.att_ids[this.att_ids.length - 1]);
      }
    },
  },
  updated: function () {
    console.log("dayleft updated");
    // this is needed to trigger the loading of the remaining days in Home.vue:day_percent_loaded
    this.$emit("percent_loaded", {
      side: "atts",
      percent: (this.loaded_att_ids.length / this.att_ids.length) * 100,
    });
  },
  created: function () {
    console.log("dayleft created");
    console.log(this.daily_record);
    this.update_me();
  },
  methods: {
    update_me: function () {
      // fetch all attendance records attached to this daily_record and add one empty one
      let att_ids = this.daily_record.attributes.attendance_record.map(
        (e) => e.id
      );
      att_ids.forEach((id) => {
        this.$set(this.start_overlaps, id, false);
        this.$set(this.end_overlaps, id, false);
        this.$set(this.too_much, id, false);
      });
      att_ids = att_ids.sort((l, r) => {
        // TODO: sort ascending by start date ?
        //       not possible here, since they are not loaded right now
        let ln = Number(l);
        let rn = Number(r);
        if (ln < rn) {
          return -1;
        } else if (ln > rn) {
          return 1;
        }
        return 0;
      });
      if (this.enabled) {
        att_ids.push(this.add_empty());
      }
      this.att_ids = att_ids;
    },
    set_error: function (att_id) {
      if (this.att_errors.indexOf(att_id) === -1) {
        this.att_errors.push(att_id);
      }
      this.$emit("valid", false);
    },
    clear_error: function (att_id) {
      this.att_errors = this.att_errors.filter((id) => id !== att_id);
      this.$emit("valid", this.att_errors.length === 0);
    },
    att_created: function (att_id) {
      this.atts[att_id].created = true;
    },
    last_is_empty: function () {
      if (this.att_ids.length === 0) {
        return false;
      }
      console.log("this.att_ids", this.att_ids);
      console.log("this.atts", this.atts);
      let last_id = this.att_ids[this.att_ids.length - 1];
      if (this.atts[last_id] === undefined) {
        return true;
      }
      return (
        this.atts[last_id].start_time === "" &&
        this.atts[last_id].end_time === "" &&
        this.atts[last_id].duration === ""
      );
    },
    last_is_incomplete: function () {
      if (this.att_ids.length === 0) {
        return false;
      }
      let last_id = this.att_ids[this.att_ids.length - 1];
      if (this.atts[last_id] === undefined) {
        return true;
      }
      return this.atts[last_id].created === false;
    },
    toggle_menu: function (event) {
      this.$refs.menu.toggle(event);
    },
    att_loaded: function (d) {
      console.log("att_loaded", d);
      this.loaded_att_ids.push(d.id);
      this.$set(this.atts, d.id, d.att);
      console.log(
        "left_loaded :",
        (this.loaded_att_ids.length / this.att_ids.length) * 100
      );
      this.$emit("percent_loaded", {
        side: "atts",
        percent: (this.loaded_att_ids.length / this.att_ids.length) * 100,
      });
    },
    add_empty: function () {
      let id = uuidv4();
      this.$set(this.start_overlaps, id, false);
      this.$set(this.end_overlaps, id, false);
      this.$set(this.too_much, id, false);
      return id;
    },
    delete_att: function (id) {
      console.log("Dayleft.delete_att", id);
      this.att_ids = this.att_ids.filter((x) => x !== id);
      console.log("att_ids is now: ", this.att_ids);
      this.loaded_att_ids = this.loaded_att_ids.filter((x) => x !== id);
      // delete this.start_overlaps[id];
      // delete this.end_overlaps[id];
      // delete this.too_much[id];

      if (this.att_ids.length === 0) {
        console.log("THIS SHOULD NOT HAPPEN !!!");
        this.att_ids.push(this.add_empty());
      } else if (this.enabeld && !this.last_is_empty()) {
        this.att_ids.push(this.add_empty());
      }
      this.update_att();
    },
    update_att: function () {
      console.log("DayLeft.update_att");
      this.verify_atts();
      this.update_sum();
      // if there are no errors in the atts, emit "sumchanged" with total sum
      if (this.atts_valid()) {
        this.$emit("sumchanged", {
          on: this.att_sum,
          off: this.att_off_sum,
          travel: this.att_travel_sum,
          refetch_daily_record: true,
        });
        this.$emit("valid", true);
      } else {
        console.log("atts not valid !!!");
        this.$emit("valid", false);
      }
    },
    work_location_by_id: function (id) {
      console.log("dl:wlbyid", id);
      for (let idx in this.work_locations) {
        if (this.work_locations[idx].id === id) {
          return this.work_locations[idx];
        }
      }
    },
    update_sum: function () {
      var sum = 0;
      var off_sum = 0;
      var travel_sum = 0;
      for (let idx in this.att_ids) {
        let id = this.att_ids[idx];
        if (this.atts[id] !== undefined) {
          // can be that it is not loaded at all
          if (
            this.work_location_by_id(this.atts[id].work_location).is_off === 1
          ) {
            console.log("skip", this.atts[id]);
            off_sum += Number(this.atts[id].duration);
            // is this possible ? is_off && travel ?
            if (
              this.work_location_by_id(this.atts[id].work_location).travel === 1
            ) {
              console.log("travel", this.atts[id]);
              travel_sum += Number(this.atts[id].duration);
            }
            continue;
          }
          if (
            this.work_location_by_id(this.atts[id].work_location).travel === 1
          ) {
            console.log("travel", this.atts[id]);
            travel_sum += Number(this.atts[id].duration);
          }
          sum += Number(this.atts[id].duration);
        }
      }
      this.att_sum = sum;
      this.att_off_sum = off_sum;
      this.att_travel_sum = travel_sum;
    },
    verify_atts: function () {
      for (let idx in this.att_ids) {
        let id = this.att_ids[idx];
        this.$set(this.start_overlaps, id, false);
        this.$set(this.end_overlaps, id, false);
        this.$set(this.too_much, id, false);
      }
      for (let idx in this.att_ids) {
        let id = this.att_ids[idx];
        let att = this.atts[id];
        this.overlaps_any(id, att);
      }
      // sort all atts by start_time
      // unify intervals that have same start_time and end_time
      // if interval > 6h -> set error on all involved atts
      let atts_ = JSON.parse(JSON.stringify(this.atts));
      let atts = [];
      for (let idx in this.att_ids) {
        atts.push(atts_[this.att_ids[idx]]);
      }
      console.log("verify_atts:", atts);
      for (let idx in atts) {
        atts[idx].start = add(this.date, {
          hours: Number(atts[idx].start_time.substr(0, 2)),
          minutes: Number(atts[idx].start_time.substr(3, 2)),
        });
        atts[idx].end = add(this.date, {
          hours: Number(atts[idx].end_time.substr(0, 2)),
          minutes: Number(atts[idx].end_time.substr(3, 2)),
        });
        atts[idx].duration_ms = atts[idx].end - atts[idx].start;
      }
      atts.sort((l, r) => l.start - r.start);
      let uuids = [];
      let last_end = null;
      let duration_ms = 0;
      for (let idx in atts) {
        let att = atts[idx];
        if (att.duration_ms === 0) {
          continue;
        }
        if (isEqual(att.start, last_end)) {
          // att directly follows att-1, sum up duration
          duration_ms = duration_ms + att.duration_ms;
          uuids.push(att.id);
          console.log(
            "franz",
            JSON.parse(JSON.stringify(uuids)),
            duration_ms / 1000 / 3600
          );
          if (duration_ms / 1000 / 3600 > 6) {
            // set error on all atts in uuids
            for (let idx in uuids) {
              console.log(idx, uuids[idx]);
              this.$set(this.too_much, uuids[idx], true);
            }
          }
        } else {
          duration_ms = att.duration_ms;
          uuids = [att.id];
        }
        last_end = att.end;
      }

      let last_id = this.att_ids[this.att_ids.length - 1];
      let last = this.atts[last_id];
      if (
        last.start !== "" &&
        last.end !== "" &&
        last.duration !== "" &&
        this.enabled
      ) {
        this.att_ids.push(this.add_empty());
      }

      console.log(atts);
      console.log(uuids);
    },
    overlaps_any: function (one_id, one) {
      console.log("overlaps_any", one_id, one);

      for (let idx in this.att_ids) {
        let other_id = this.att_ids[idx];
        if (one_id === other_id) {
          continue;
        }
        console.log(other_id);
        let other = this.atts[other_id];
        let interval_one = {
          start: add(this.date, {
            hours: Number(one.start_time.substr(0, 2)),
            minutes: Number(one.start_time.substr(3, 2)),
          }),
          end: add(this.date, {
            hours: Number(one.end_time.substr(0, 2)),
            minutes: Number(one.end_time.substr(3, 2)),
          }),
        };
        let interval_other = {
          start: add(this.date, {
            hours: Number(other.start_time.substr(0, 2)),
            minutes: Number(other.start_time.substr(3, 2)),
          }),
          end: add(this.date, {
            hours: Number(other.end_time.substr(0, 2)),
            minutes: Number(other.end_time.substr(3, 2)),
          }),
        };
        if (areIntervalsOverlapping(interval_one, interval_other)) {
          console.log("intervals are overlapping");
          console.log(interval_one);
          console.log(interval_other);
          if (isAfter(interval_other.start, interval_one.start)) {
            if (isAfter(interval_one.end, interval_other.start)) {
              console.log(one_id + " end " + other_id + " start overlaps");
              //this.$set(this.start_omy_day.atts, index, Object.assign ({end_overlaps: true}, this.atts[index]))
              //this.att_by_uuid(one.data.id).end_overlaps = true
              this.$set(this.end_overlaps, one_id, true);
              //this.att_by_uuid(other.data.id).start_overlaps = true
              this.$set(this.start_overlaps, other_id, true);
            } else if (isAfter(interval_one.start, interval_other.end)) {
              console.log(one_id + " start " + other_id + " end overlaps");
              //this.att_by_uuid(one.data.id).start_overlaps = true
              //this.att_by_uuid(other.data.id).end_overlaps = true
            }
          } else if (isEqual(interval_one.start, interval_other.start)) {
            console.log("sandre");
            this.$set(this.start_overlaps, one_id, true);
            this.$set(this.start_overlaps, other_id, true);
          }
          return other_id;
        }
      }
    },
    atts_valid: function () {
      for (let idx in this.att_ids) {
        let id = this.att_ids[idx];
        if (
          this.start_overlaps[id] ||
          this.end_overlaps[id] ||
          this.too_much[id]
        ) {
          return false;
        }
      }
      return true;
    },
  },
  computed: {
    ...mapState("rest", [
      "created_attendance_record",
      "attendance_records",
      "work_locations",
    ]),
    enabled: function () {
      return (
        this.enabled_from_above &&
        this.daily_record.attributes.status.id ===
          defines.daily_record_status.open
      );
    },
    date: function () {
      return new Date(this.daily_record.attributes.date.replace(".", "T"));
    },
    all_atts_loaded: function () {
      for (let id in this.att_ids) {
        if (this.loaded_att_ids.indexOf(this.att_ids[id]) === -1) {
          return false;
        }
      }
      return true;
    },
  },
};
</script>

<style scoped>
.t5-menu {
  width: 14rem;
}
</style>
