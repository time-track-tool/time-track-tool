<template>
  <div>
    <div
      class="border-tb p-d-flex p-jc-start p-ai-center p-highlight"
      :style="day_is_weekend ? 'background: var(--surface-border)' : ''"
      style="
        padding-top: 1em;
        padding-bottom: 1em;
        margin-bottom: 1em;
        height: 4.5em;
      "
    >
      <div class="w5 tc p-ml-2" :class="enabled ? '' : 'p-disabled'">
        <Tag
          :severity="
            sums_equal
              ? 'success'
              : tr_sum + tr_off_no_durations_allowed_sum === 0 && day_is_empty
              ? 'info'
              : 'danger'
          "
          :id="'tr_sum_' + daily_record.id"
          v-bind:class="{
            animate__animated: animate,
            animate__bounceIn: animate,
          }"
          >&Sigma; {{ tr_sum }}h</Tag
        >
      </div>
      <div
        :class="enabled ? '' : 'p-disabled'"
        style="flex-grow: 1; font-weight: bold"
      >
        What did you do?
      </div>
      <div class="">
        <!-- <Button
          v-if="dr_is_status_open"
          :disabled="!submit_enabled"
          type="button"
          label="Update from Jira"
          class="p-mr-2 p-button-secondary"
        /> -->
        <InlineMessage v-if="submit_error" severity="error">{{
          submit_error
        }}</InlineMessage>
        <Button
          v-if="dr_is_status_open && submit_enabled"
          :disabled="!submit_enabled"
          type="button"
          label="Submit"
          class="p-button-success p-mr-3"
          @click="$emit('submit')"
        />
        <Button
          v-else-if="dr_is_status_submitted"
          :disabled="!submit_enabled"
          type="button"
          label="Edit again"
          class="p-button-success p-mr-3 p-button-outlined"
          @click="$emit('editagain')"
        />
        <template v-else>
          <Button
            v-if="is_frozen"
            type="button"
            style="text-transform: capitalize"
            label="Frozen"
            class="p-button-info p-mr-3"
            disabled
          />
          <Button
            v-else
            type="button"
            style="text-transform: capitalize"
            :label="daily_record.attributes.status.name"
            class="p-button-info p-mr-3"
            disabled
          />
        </template>
      </div>
    </div>
    <TimeRecs
      v-for="(tr_id, idx) in tr_ids"
      v-bind:daily_record_id="daily_record.id"
      v-bind:tr_id="tr_id"
      v-bind:enabled="enabled"
      v-bind:float_labels="idx === 0"
      v-bind:wps="wps"
      v-bind:date="date"
      v-bind:is_last="idx === tr_ids.length - 1"
      v-bind:error_msg="error_messages[tr_id]"
      :key="'tr_' + tr_id"
      @update="update_tr"
      @delete="delete_tr"
      @loaded="tr_loaded"
      @created="tr_created"
      @set_error="set_error"
      @clear_error="clear_error"
    />
  </div>
</template>

<script>
import TimeRecs from "./TimeRecs.vue";
import { format } from "date-fns";
import { v4 as uuidv4 } from "uuid";
import { mapActions, mapState } from "vuex";
import defines from "../defines";

export default {
  name: "DayRight",
  props: {
    daily_record: { type: Object, required: true },
    submit_enabled: { type: Boolean, required: true },
    sums_equal: { type: Boolean, required: true },
    update: { type: Boolean, required: true },
    enabled_from_above: { type: Boolean, required: true },
    day_is_empty: { type: Boolean, required: true },
    submit_error: { type: String, required: true },
    daily_work_hours: { type: Number, required: true },
    is_first: { type: Boolean, required: true },
    day_is_weekend: { type: Boolean, required: true },
  },
  data: function () {
    return {
      tr_ids: [],
      tr_sum: 0,
      tr_off_sum: 0,
      tr_off_no_durations_allowed_sum: 0,
      tr_travel_sum: 0,
      trs: {},
      wps: [],
      tr_errors: [],
      wps_by_id: {},
      format_date: format,
      loaded_tr_ids: [],
      animate: false,
      error_messages: {},
    };
  },
  components: {
    TimeRecs,
  },
  xxupdated: function () {
    console.log("dayright updated");
    if (this.trs.length === 0) {
      this.add_empty();
    } else {
      let last = this.trs[this.trs.length - 1];
      if (last.wp_id !== null && last.duration !== "") {
        this.add_empty();
      }
    }
  },
  created: function () {
    console.log("dayright created");
    this.update_me();
  },
  watch: {
    tr_sum: function () {
      this.animate = true;
      document
        .getElementById("tr_sum_" + this.daily_record.id)
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
        console.log("right:i should update myself");
        this.update_me();
      } else {
        console.log("right:skip update");
      }
    },
    all_trs_loaded: function () {
      if (this.all_trs_loaded === true) {
        this.update_sum();
        this.$emit("sumchanged", {
          on: this.tr_sum,
          off: this.tr_off_sum,
          off_no_durations_allowed: this.tr_off_no_durations_allowed_sum,
          travel: this.tr_travel_sum,
          refetch_daily_record: false,
        });
      }
    },
    enabled: function () {
      if (this.enabled && !this.last_is_empty()) {
        this.tr_ids.push(this.add_empty());
      } else if (
        !this.enabled &&
        (this.last_is_empty() || this.last_is_incomplete())
      ) {
        this.delete_tr(this.tr_ids[this.tr_ids.length - 1]);
      }
    },
  },
  methods: {
    ...mapActions("rest", [
      "fetch_time_record",
      "fetch_my_time_wps",
      "fetch_public_time_wps",
    ]),
    set_error: function (tr_id) {
      if (this.tr_errors.indexOf(tr_id) === -1) {
        this.tr_errors.push(tr_id);
      }
      this.$emit("valid", false);
    },
    clear_error: function (tr_id) {
      this.tr_errors = this.tr_errors.filter((id) => id !== tr_id);
      this.$emit("valid", this.tr_errors.length === 0);
    },
    update_me: function () {
      // wps: [{
      //     "tc_wp_id": "2068_31198",
      //     "tc_name": "Pre-Sales-Auto-Europe",
      //     "wp_name": "Bosch MW-Better (2020)"
      // },]
      this.tr_ids = [];
      this.tr_sum = 0;
      this.tr_off_sum = 0;
      this.tr_off_no_durations_allowed_sum = 0;
      this.tr_travel_sum = 0;
      this.trs = {};
      this.wps = [];
      this.tr_errors = [];
      this.wps_by_id = {};
      this.format_date = format;
      this.loaded_tr_ids = [];
      this.animate = false;
      this.error_messages = {};
      let wps = [];
      let off_wps = [];
      this.fetch_my_time_wps({
        params: {
          user_id: this.user_id,
          date_str: format(this.date, "yyyy-MM-dd"),
        },
      }).then((resp) => {
        if (resp.status === 200) {
          resp.data.data.collection.forEach((element) => {
            let wp = {
              // id: element["project.id"] + "_" + element.id,
              id: element.id,
              tc_name: element["project.name"],
              wp_name: element.name,
              name: element["project.name"] + " - " + element.name,
              is_public_holiday: element["project.is_public_holiday"],
              is_vacation: element["project.is_vacation"] === 1,
              is_off: element["project.work_location.is_off"] === 1,
              is_special_leave: element["project.is_special_leave"] === 1,
              no_overtime_day: element["project.no_overtime_day"] === 1,
              max_hours: element["project.max_hours"],
              durations_allowed: element["durations_allowed"],
            };
            if (wp.is_off === true) {
              off_wps.push(wp);
            } else {
              wps.push(wp);
            }
            this.wps_by_id[wp.id] = wp;
          });

          this.fetch_public_time_wps({
            params: {
              date_str: format(this.date, "yyyy-MM-dd"),
            },
          }).then((resp) => {
            resp.data.data.collection.forEach((element) => {
              let wp = {
                // id: element["project.id"] + "_" + element.id,
                id: element.id,
                tc_name: element["project.name"],
                wp_name: element.name,
                name: element["project.name"] + " - " + element.name,
                is_public_holiday: element["project.is_public_holiday"],
                is_vacation: element["project.is_vacation"] === 1,
                is_off: element["project.work_location.is_off"] === 1,
                is_special_leave: element["project.is_special_leave"] === 1,
                no_overtime_day: element["project.no_overtime_day"] === 1,
                max_hours: element["project.max_hours"],
                durations_allowed: element["durations_allowed"],
              };
              if (wp.is_off === true) {
                off_wps.push(wp);
              } else {
                wps.push(wp);
              }
              this.wps_by_id[wp.id] = wp;

              let tr_ids = this.daily_record.attributes.time_record.map(
                (e) => e.id
              );
              tr_ids = tr_ids.sort((l, r) => {
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
                tr_ids.push(this.add_empty());
              }
              this.tr_ids = tr_ids;
            });
            wps.forEach((wp) => this.wps.push(wp));
            off_wps.forEach((wp) => this.wps.push(wp));
          });
        }
      });
    },
    tr_loaded: function (d) {
      console.log("tr_loaded", d);
      this.loaded_tr_ids.push(d.id);
      this.$set(this.trs, d.id, d.tr);
      this.$set(this.error_messages, d.id, "");
      console.log(
        "right_loaded:",
        (this.loaded_tr_ids.length / this.tr_ids.length) * 100
      );
      this.$emit("percent_loaded", {
        side: "trs",
        percent: (this.loaded_tr_ids.length / this.tr_ids.length) * 100,
      });
    },
    tr_created: function (tr_id) {
      this.trs[tr_id].created = true;
    },
    add_empty: function () {
      let uuid = uuidv4();
      return uuid;
    },
    delete_tr: function (id) {
      console.log("Dayright.delete_tr", id);
      this.tr_ids = this.tr_ids.filter((x) => x !== id);
      console.log("tr_ids is now: ", this.tr_ids);
      this.loaded_tr_ids = this.loaded_tr_ids.filter((x) => x !== id);

      if (this.tr_ids.length === 0) {
        console.log("TR: THIS SHOULD NOT HAPPEN !!!");
        this.tr_ids.push(this.add_empty());
      } else if (this.enabled && !this.last_is_empty()) {
        this.tr_ids.push(this.add_empty());
      }
      this.update_sum();
      this.$emit("sumchanged", {
        on: this.tr_sum,
        off: this.tr_off_sum,
        off_no_durations_allowed: this.tr_off_no_durations_allowed_sum,
        travel: this.tr_travel_sum,
        refetch_daily_record: true,
      });
    },
    last_is_empty: function () {
      if (this.tr_ids.length === 0) {
        return false;
      }
      let last_id = this.tr_ids[this.tr_ids.length - 1];
      if (this.trs[last_id] === undefined) {
        return true;
      }
      return (
        this.trs[last_id].comment === "" &&
        this.trs[last_id].duration === "" &&
        this.trs[last_id].time_activity_id === "normal_work" &&
        (this.trs[last_id].wp_id === null || this.trs[last_id].wp === "")
      );
    },
    last_is_incomplete: function () {
      if (this.tr_ids.length === 0) {
        return false;
      }
      let last_id = this.tr_ids[this.tr_ids.length - 1];
      if (this.trs[last_id] === undefined) {
        return true;
      }
      return this.trs[last_id].created === false;
    },
    add_empty_if_last_is_not_empty: function () {
      if (!this.last_is_empty()) {
        this.tr_ids.push(this.add_empty());
      }
    },
    update_tr: function () {
      console.log("update_trs");
      this.add_empty_if_last_is_not_empty();
      this.verify_trs();
      this.update_sum();
      this.$emit("sumchanged", {
        on: this.tr_sum,
        off: this.tr_off_sum,
        off_no_durations_allowed: this.tr_off_no_durations_allowed_sum,
        travel: this.tr_travel_sum,
        refetch_daily_record: true,
      });
    },
    update_sum: function () {
      let sum = 0;
      let off_sum = 0;
      let tr_off_no_durations_allowed_sum = 0;
      let travel_sum = 0;
      for (let idx in this.tr_ids) {
        let id = this.tr_ids[idx];
        if (this.trs[id] !== undefined) {
          // can be that it is not loaded at all
          if (this.trs[id].wp.is_off === true) {
            console.log("skip", this.trs[id]);
            off_sum += Number(this.trs[id].duration);
            if (this.trs[id].wp.durations_allowed === 0) {
              tr_off_no_durations_allowed_sum += Number(this.trs[id].duration);
            }
            // is this possible ? is_off && travel ?
            if (
              this.time_activity_by_id(this.trs[id].time_activity_id).travel ===
              1
            ) {
              console.log("travel", this.trs[id]);
              travel_sum += Number(this.trs[id].duration);
            }
            continue;
          }
          if (
            this.time_activity_by_id(this.trs[id].time_activity_id).travel === 1
          ) {
            console.log("travel", this.trs[id]);
            travel_sum += Number(this.trs[id].duration);
          }

          sum += Number(this.trs[id].duration);
        }
      }
      this.tr_sum = sum;
      this.tr_off_sum = off_sum;
      this.tr_off_no_durations_allowed_sum = tr_off_no_durations_allowed_sum;
      this.tr_travel_sum = travel_sum;
      this.verify_trs();
    },
    time_activity_by_id: function (id) {
      for (let idx in this.time_activities) {
        if (this.time_activities[idx].id === id) {
          return this.time_activities[idx];
        }
      }
    },
    verify_trs: function () {
      // check if we have no_overtime_day vs daily_work_hours
      let valid = true;
      let no_overtime_wp = false;
      for (let idx in this.trs) {
        if (this.trs[idx].wp.no_overtime_day === true) {
          no_overtime_wp = true;
          break;
        }
      }
      if (
        no_overtime_wp === true &&
        this.tr_sum + this.tr_off_sum > this.daily_work_hours
      ) {
        let msg =
          "because of this WP, total time must not exceed " +
          this.daily_work_hours;
        valid = false;
        for (let idx in this.trs) {
          if (this.trs[idx].wp.no_overtime_day === true) {
            this.error_messages[idx] = msg;
          } else {
            this.error_messages[idx] = "";
          }
        }
      } else {
        // clear error messages
        for (let idx in this.trs) {
          this.error_messages[idx] = "";
        }
      }
      console.log("verify_trs", valid);

      this.$emit("valid", valid);
    },
  },
  computed: {
    ...mapState(["user_id"]),
    ...mapState("rest", [
      "vacation_correction",
      "time_activities",
      "frozen_until",
    ]),
    is_frozen: function () {
      return this.date <= this.frozen_until;
    },
    all_trs_loaded: function () {
      for (let id in this.tr_ids) {
        if (this.loaded_tr_ids.indexOf(this.tr_ids[id]) === -1) {
          return false;
        }
      }
      return true;
    },
    enabled: function () {
      return (
        this.enabled_from_above &&
        this.daily_record.attributes.status.id ===
          defines.daily_record_status.open
      );
    },
    dr_is_status_open: function () {
      return (
        this.daily_record.attributes.status.id ===
        defines.daily_record_status.open
      );
    },
    dr_is_status_submitted: function () {
      return (
        this.daily_record.attributes.status.id ===
          defines.daily_record_status.submitted && !this.is_frozen
      );
    },
    date: function () {
      return new Date(this.daily_record.attributes.date.replace(".", "T"));
    },
  },
};
</script>
