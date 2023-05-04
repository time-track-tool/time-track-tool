<template>
  <div>
    <template v-if="update_daily_record_error[daily_record_id]">
      <Message
        v-for="message in update_daily_record_error[daily_record_id].split(
          '\n'
        )"
        :key="message"
        severity="error"
        :closable="false"
        >{{ message }}</Message
      >
    </template>
    <Message v-if="error" severity="warn" :closable="false">{{
      error
    }}</Message>
    <div class="p-grid">
      <div
        v-if="daily_record_fetched === true"
        class="p-col p-pr-0"
        style="
          border-right: 1px solid var(--surface-d);
          margin-top: 0.5rem;
          padding-top: 0px;
        "
      >
        <div class="box">
          <DayLeft
            v-bind:daily_record="daily_record"
            v-bind:is_first="is_first"
            v-bind:sums_equal="sums_equal"
            v-bind:update="update_day_left"
            v-bind:enabled_from_above="day_enabled && enable_day_left"
            v-bind:day_is_empty="sums_empty"
            v-bind:day_is_weekend="day_is_weekend"
            v-on:sumchanged="att_sum_changed"
            v-on:copy_from_last_day="copy_from_last_day"
            v-on:copy_day_to_month="copy_day_to_month"
            v-on:copy_day_to_week="copy_day_to_week"
            v-on:copy_from_last_week="copy_from_last_week"
            @percent_loaded="total_percent_loaded"
            @valid="valid_from_atts"
          />
        </div>
      </div>
      <div v-if="daily_record_fetched === true" class="p-col p-pl-0">
        <div class="box">
          <DayRight
            v-bind:daily_record="daily_record"
            v-bind:sums_equal="sums_equal"
            v-bind:submit_enabled="submit_enabled"
            v-bind:submit_error="submit_error"
            v-bind:update="update_day_right"
            v-bind:enabled_from_above="day_enabled && enable_day_right"
            v-bind:day_is_empty="sums_empty"
            v-bind:daily_work_hours="daily_work_hours"
            v-bind:is_first="is_first"
            v-bind:day_is_weekend="day_is_weekend"
            v-on:sumchanged="tr_sum_changed"
            @editagain="edit_again"
            @submit="submit_day"
            @percent_loaded="total_percent_loaded"
            @valid="valid_from_trs"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DayLeft from "@/components/DayLeft.vue";
import DayRight from "@/components/DayRight.vue";
import { mapActions, mapState } from "vuex";
import { format, sub, isEqual, parseISO } from "date-fns";
import isWeekend from "date-fns/isWeekend";
import defines from "../defines";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Day",
  props: {
    day: { type: Date, required: true },
    is_first: { type: Boolean, required: true },
    copy_from_daily_record: { type: Object, required: false },
    submit_from_above: { type: Boolean, required: false },
    edit_again_from_above: { type: Boolean, required: false },
  },
  data: function () {
    return {
      daily_record_id: null,
      date_string: format(this.day, "yyyy-MM-dd"),
      daily_record_fetched: false,
      att_sum: { on: 0, off: 0 },
      tr_sum: { on: 0, off: 0 },
      trs_valid: true,
      atts_valid: true,
      error: null,
      submit_error: "",
      loaded_percent: 0,
      loaded_percent_by_side: { atts: 0, trs: 0 },
      update_day_left: false,
      enable_day_left: true,
      update_day_right: false,
      enable_day_right: true,
      user_dynamic_fetched: false,
      submit_enabled: false,
    };
  },
  components: {
    DayLeft,
    DayRight,
  },
  created: function () {
    this.find_user_dynamic({
      params: { user_id: this.user_id, date_str: this.date_string },
    }).then(() => {
      if (this.user_dynamic_id_for_date[this.date_string] === null) {
        this.error =
          "Booking not possible, no user_dynamic record for: " + this.day;
        // to continue loading of the remaining days:
        this.$emit("percent_loaded", {
          day: this.day,
          percent: 100,
        });
      } else {
        if (this.user_dynamic[this.date_string] === undefined) {
          this.fetch_user_dynamic({
            params: {
              id: this.user_dynamic_id_for_date[this.date_string],
              date_str: this.date_string,
            },
          }).then(() => this.created_2());
        } else {
          this.created_2();
        }
      }
    });
  },
  updated: function () {
    console.log("day updated");
  },

  methods: {
    ...mapActions("rest", [
      "find_daily_record",
      "fetch_daily_record",
      "create_daily_record",
      "update_daily_record",
      "find_user_dynamic",
      "fetch_user_dynamic",
      "search_vacation_correction",
      "delete_attendance_record",
      "create_attendance_record",
      "delete_time_record",
      "create_time_record",
    ]),
    created_2: function () {
      this.user_dynamic_fetched = true;
      if (this.user_dynamic[this.date_string].booking_allowed !== 1) {
        this.error = "booking is not allowed for user" + this.user_id;
      } else {
        this.error = null;
      }
      let ct_filter = "-1";
      if (this.user_dynamic[this.date_string].contract_type !== null) {
        ct_filter = this.user_dynamic[this.date_string].contract_type.id;
      }
      if (this.error === null) {
        this.search_vacation_correction({
          params: {
            user_id: this.user_id,
            date_str: this.date_string,
            contract_type: ct_filter,
          },
        }).then(() => {
          this.find_daily_record({
            params: { date: this.date_string, user_id: this.user_id },
          }).then(() => {
            if (this.found_daily_record_id) {
              console.log("found id:", this.found_daily_record_id);
              this.daily_record_id = this.found_daily_record_id;
              this.fetch_daily_record({
                params: { id: this.daily_record_id },
              }).then(() => {
                this.daily_record_fetched = true;
                this.update_submit_enabled();
                if (!this.day_enabled) {
                  this.$emit("percent_loaded", {
                    day: this.day,
                    percent: 100,
                  });
                }
              });
            } else {
              console.log("no id found, create daily record");
              this.create_daily_record({
                data: {
                  user: this.user_id,
                  date: this.date_string + ".00:00:00",
                },
              }).then(() => {
                if (this.created_daily_record_id !== null) {
                  this.daily_record_id = this.created_daily_record_id;
                  this.fetch_daily_record({
                    params: { id: this.daily_record_id },
                  }).then(() => {
                    this.daily_record_fetched = true;
                    this.update_submit_enabled();
                    if (!this.day_enabled) {
                      this.$emit("percent_loaded", {
                        day: this.day,
                        percent: 100,
                      });
                    }
                  });
                } else {
                  this.error = "creating daily record failed !";
                }
              });
            }
          });
        });
      }
    },
    copy_from_last_day: function (data) {
      let prev_date = sub(this.day, { days: 1 });
      let prev_daily_record = null;
      for (let k in this.daily_records) {
        let dr_date = parseISO(
          this.daily_records[k].attributes.date.split(".")[0]
        );
        if (isEqual(prev_date, dr_date)) {
          prev_daily_record = this.daily_records[k];
          break;
        }
      }
      if (prev_daily_record === null) {
        this.error = "failed to find daily_record of last day";
      } else {
        this.from_daily_record(prev_daily_record, data);
      }
    },
    from_daily_record: function (daily_record, opts) {
      console.log(
        "from_daily_record",
        this.daily_record_id,
        daily_record,
        opts
      );

      if (daily_record.id === this.daily_record_id) {
        console.log("i wont copy me over myself !");
        return;
      }

      if (
        daily_record.attributes.status.id === defines.daily_record_status.leave
      ) {
        console.log("WONT COPY VACATION ENTRIES");
        return;
      }

      if (isWeekend(this.day) && this.day_enabled === false) {
        console.log("WEEKEND BOOKING NOT ALLOWED");
        return;
      }

      if (
        this.daily_record.attributes.status.id ===
        defines.daily_record_status.submitted
      ) {
        console.log("I AM ALREADY SUBMITTED - no changes allowed");
        return;
      }

      // if data.copy_atts == true
      if (opts.copy_atts) {
        this.enable_day_left = false;
        //   clear current daily record's atts
        let att_delete_promises = [];
        this.daily_record.attributes.attendance_record.forEach((att) => {
          if (
            this.attendance_records[att.id].attributes[
              "time_record.wp.durations_allowed"
            ] !== 1
          ) {
            att_delete_promises.push(
              this.delete_attendance_record({
                data: { "@etag": this.attendance_records[att.id]["@etag"] },
                params: { id: att.id },
              })
            );
          }
        });
        Promise.all(att_delete_promises).then(() => {
          // create new atts and store for this daily record
          // we assume that prev_daily_record's atts already have been loaded
          let att_create_promises = [];
          daily_record.attributes.attendance_record.forEach((att) => {
            let att_data = this.attendance_records[att.id].attributes;
            if (att_data["time_record.wp.durations_allowed"] !== 1) {
              att_create_promises.push(
                this.create_attendance_record({
                  data: {
                    start: att_data.start,
                    end: att_data.end,
                    daily_record: this.daily_record_id,
                    work_location: att_data.work_location,
                  },
                })
              );
            }
          });
          Promise.all(att_create_promises).then(() => {
            this.fetch_daily_record({
              params: { id: this.daily_record_id },
            }).then(() => {
              this.update_day_left = true;
              this.enable_day_left = true;
              this.update_submit_enabled();
            });
          });
        });
      }
      // if data.copy_trs == true
      if (opts.copy_trs) {
        this.enable_day_right = false;
        //   clear current daily record's trs
        let tr_delete_promises = [];
        this.daily_record.attributes.time_record.forEach((tr) => {
          if (
            this.time_records[tr.id].attributes[
              "wp.project.is_public_holiday"
            ] !== 1
          ) {
            tr_delete_promises.push(
              this.delete_time_record({
                data: { "@etag": this.time_records[tr.id]["@etag"] },
                params: { id: tr.id },
              })
            );
          }
        });
        Promise.all(tr_delete_promises).then(() => {
          // create new trs and store for this daily record
          // we assume that prev_daily_record's trs already have been loaded
          let tr_create_promises = [];
          daily_record.attributes.time_record.forEach((tr) => {
            let tr_data = this.time_records[tr.id].attributes;
            if (tr_data["wp.project.is_public_holiday"] !== 1) {
              let d = {
                duration: tr_data.duration,
                wp: tr_data["wp.id"],
                daily_record: this.daily_record_id,
              };
              if (tr_data["time_activity.id"] !== null) {
                d.time_activity = tr_data["time_activity.id"];
              }
              if (tr_data.comment) {
                d.comment = tr_data.comment;
              }
              tr_create_promises.push(
                this.create_time_record({
                  data: d,
                })
              );
            }
          });
          Promise.all(tr_create_promises).then(() => {
            this.fetch_daily_record({
              params: { id: this.daily_record_id },
            }).then(() => {
              this.update_day_right = true;
              this.enable_day_right = true;
              this.update_submit_enabled();
            });
          });
        });
      }
    },
    copy_from_last_week: function (opts) {
      this.$emit("copy_from_last_week", { opts: opts }); // upstream knows what week is displayed
    },
    copy_day_to_month: function (opts) {
      this.$emit("copy_day_to_month", {
        daily_record: this.daily_record,
        opts: opts,
      });
    },
    copy_day_to_week: function (opts) {
      this.$emit("copy_day_to_week", {
        daily_record: this.daily_record,
        opts: opts,
      });
    },
    total_percent_loaded: function (data) {
      this.loaded_percent_by_side[data.side] = data.percent;
      this.loaded_percent =
        (this.loaded_percent_by_side.atts + this.loaded_percent_by_side.trs) /
        2;
      console.log("day_loaded: ", this.loaded_percent);
      this.$emit("percent_loaded", {
        day: this.day,
        percent: this.loaded_percent,
      });
      this.update_day_left = false;
      this.update_day_right = false;
    },
    att_sum_changed: function (att_sum) {
      this.att_sum = att_sum;
      if (this.loaded_percent >= 100) {
        if (this.off_time_correct()) {
          if (this.travel_time_correct()) {
            this.update_submit_enabled();
          }
        }
      }
      // to refresh the etag header
      if (att_sum.refetch_daily_record) {
        this.fetch_daily_record({ params: { id: this.daily_record_id } }).then(
          () => {
            this.$emit("att_sum_changed", { day: this.day, sum: this.att_sum });
          }
        );
      } else {
        this.$emit("att_sum_changed", { day: this.day, sum: this.att_sum });
      }
    },
    tr_sum_changed: function (tr_sum) {
      this.tr_sum = tr_sum;
      if (this.loaded_percent >= 100) {
        if (this.off_time_correct()) {
          if (this.travel_time_correct()) {
            this.update_submit_enabled();
          }
        }
      }
      if (tr_sum.refetch_daily_record) {
        this.fetch_daily_record({ params: { id: this.daily_record_id } });
      }
    },
    valid_from_atts: function (validity) {
      this.atts_valid = validity;
      this.update_submit_enabled();
    },
    valid_from_trs: function (validity) {
      this.trs_valid = validity;
      this.update_submit_enabled();
    },
    submit_day: function () {
      console.log("set status of daily_record to submitted");
      this.update_daily_record({
        data: {
          "@etag": this.daily_record["@etag"],
          status: "submitted",
        },
        params: { id: this.daily_record.id },
      }).then((resp) => {
        this.fetch_daily_record({ params: { id: resp.data.data.id } }).then(
          () => this.emit_status()
        );
      });
    },
    edit_again: function () {
      console.log(
        "set status of daily record to open if it is in status subitted"
      );
      this.update_daily_record({
        data: {
          "@etag": this.daily_record["@etag"],
          status: "open",
        },
        params: { id: this.daily_record.id },
      }).then((resp) => {
        this.fetch_daily_record({ params: { id: resp.data.data.id } }).then(
          () => this.emit_status()
        );
      });
    },
    off_time_correct: function () {
      let res = true;
      if (
        this.tr_sum.off_no_durations_allowed > 0 &&
        this.att_sum.off < this.tr_sum.off_no_durations_allowed
      ) {
        this.submit_error =
          "You need to have " +
          this.tr_sum.off_no_durations_allowed +
          " hours Off time";
        res = false;
      } else if (this.att_sum.off > 0 || this.tr_sum.off > 0) {
        if (this.att_sum.off > this.tr_sum.off) {
          this.submit_error =
            'You can\'t have more "Off/Absent" time on the left than on the right';
          res = false;
        } else {
          this.submit_error = "";
        }
      } else {
        this.submit_error = "";
      }
      return res;
    },
    travel_time_correct: function () {
      let res = true;
      if (this.att_sum.travel > 0 || this.tr_sum.travel > 0) {
        if (this.att_sum.travel === this.tr_sum.travel) {
          this.submit_error = "";
        } else {
          this.submit_error =
            "You must have the same amount of travel time on both sides";
          res = false;
        }
      } else {
        this.submit_error = "";
      }
      return res;
    },
    emit_status: function () {
      this.$emit("status", {
        key: this.date_string,
        data: {
          submittable:
            this.submit_enabled &&
            this.daily_record.attributes.status.id ===
              defines.daily_record_status.open,
          submitted:
            this.daily_record.attributes.status.id ===
            defines.daily_record_status.submitted,
          is_frozen: this.is_frozen,
        },
      });
    },
    update_submit_enabled: function () {
      this.submit_enabled =
        this.sums_equal &&
        this.off_time_correct() &&
        this.travel_time_correct() &&
        this.trs_valid &&
        this.atts_valid;
      this.emit_status();
    },
  },
  computed: {
    ...mapState(["user_id"]),
    ...mapState("rest", [
      "found_daily_record_id",
      "daily_records",
      "created_daily_record_id",
      "update_daily_record_error",
      "user_dynamic",
      "user_dynamic_id_for_date",
      "attendance_records",
      "time_records",
      "frozen_until",
    ]),
    is_frozen: function () {
      return this.day <= this.frozen_until;
    },
    daily_record: function () {
      return this.daily_records[this.daily_record_id];
    },
    daily_work_hours: function () {
      let user_dynamic = this.user_dynamic[this.date_string];
      return user_dynamic["hours_" + format(this.day, "E").toLowerCase()];
    },
    sums_equal: function () {
      if (this.att_sum.on > 0 || this.tr_sum.on > 0) {
        return this.att_sum.on === this.tr_sum.on && this.off_time_correct();
      } else if (this.att_sum.on === 0 && this.tr_sum.off > 0) {
        return this.off_time_correct();
      } else {
        return false;
      }
    },
    sums_empty: function () {
      return (
        this.att_sum.on === 0 &&
        this.tr_sum.on === 0 &&
        this.tr_sum.off_no_durations_allowed === 0
      );
    },
    day_enabled: function () {
      if (!isWeekend(this.day)) {
        return true;
      } else {
        if (this.daily_record_fetched === true) {
          if (this.daily_record.attributes.weekend_allowed === 1) {
            return true;
          } else {
            if (this.user_dynamic_fetched === true) {
              if (this.user_dynamic[this.date_string].weekend_allowed === 1) {
                return true;
              }
            }
          }
        }
      }
      return false;
    },
    day_is_weekend: function () {
      return isWeekend(this.day);
    },
  },
  watch: {
    copy_from_daily_record: function () {
      if (this.copy_from_daily_record !== undefined) {
        this.from_daily_record(
          this.copy_from_daily_record.daily_record,
          this.copy_from_daily_record.opts
        );
      }
    },
    submit_from_above: function () {
      if (
        this.submit_from_above === true &&
        this.submit_enabled === true &&
        this.daily_record.attributes.status.id ===
          defines.daily_record_status.open &&
        !this.is_frozen
      ) {
        this.submit_day();
      }
    },
    edit_again_from_above: function () {
      if (
        this.edit_again_from_above === true &&
        this.daily_record.attributes.status.id ===
          defines.daily_record_status.submitted &&
        !this.is_frozen
      ) {
        this.edit_again();
      }
    },
  },
};
</script>

<style scoped>
div.np {
  padding-left: 0px;
  padding-right: 0px;
}
</style>
