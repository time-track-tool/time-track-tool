<template>
  <div class="home">
    <div class="p-p-3 p-formgroup-inline">
      <div class="p-field">
        <span class="p-buttonset">
          <Button
            label="<"
            @click="decrement_interval"
            :disabled="$route.params.range === 'range' ? true : false"
          />
          <Button :label="range_display" class="p-button-success" />
          <Button
            label=">"
            @click="increment_interval"
            :disabled="$route.params.range === 'range' ? true : false"
          />
        </span>
      </div>
      <div class="p-field">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon" id="week"> Week: </span>
          <Calendar
            v-model="calendar_value_week"
            @date-select="calendar_week_changed"
            selectionMode="single"
            showWeek
            dateFormat="dd.mm.yy"
            :manualInput="false"
            showIcon
            appendTo="week"
          />
        </div>
      </div>
      <div class="p-field">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon"> Month: </span>
          <Calendar
            v-model="calendar_value_month"
            @date-select="calendar_month_changed"
            selectionMode="single"
            :manualInput="false"
            dateFormat="dd.mm.yy"
            view="month"
            showIcon
          />
        </div>
      </div>
      <div class="p-field">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon"> Range: </span>
          <Calendar
            ref="range_picker"
            v-model="calendar_value_range"
            showWeek
            @date-select="calendar_range_changed"
            selectionMode="range"
            dateFormat="dd.mm.yy"
            :manualInput="false"
            showIcon
          />
        </div>
      </div>
    </div>

    <ProgressBar
      :value="percent_loaded"
      :showValue="false"
      style="height: 0.5em"
    />

    <Day
      v-for="(day, idx) in days"
      v-bind:day="day"
      v-bind:is_first="idx === 0"
      v-bind:copy_from_daily_record="daily_record_to[day]"
      v-bind:submit_from_above="submit_all"
      v-bind:edit_again_from_above="edit_again_all"
      :key="day.toString()"
      v-on:copy_day_to_week="copy_day_to_week"
      v-on:copy_day_to_month="copy_day_to_month"
      v-on:copy_from_last_week="copy_from_last_week"
      v-on:att_sum_changed="att_sum_changed"
      @percent_loaded="day_percent_loaded"
      @status="register_daily_record_status"
    />

    <Dialog
      v-if="api_error.who !== ''"
      :header="'REST Api Error in ' + api_error.who"
      :visible="api_error.who !== ''"
      :modal="true"
      :closable="false"
    >
      {{ api_error.error }}
      <br />
      <br />
      Please reload the page, if the problem persists, please report by making a
      screenshot.

      <pre>
  
uri: {{ api_error.error.config.url }}

msg: {{ api_error.error.response.data.error.msg }}
</pre
      >
    </Dialog>

    <div class="border p-p-3 p-d-flex p-jc-between">
      <Button :label="'v' + version" class="p-mr-2 p-button-info" disabled />
      <Button
        v-if="$route.params.range === 'week'"
        :label="'Total: ' + att_sum_for_days + 'h'"
        class="p-mr-2 p-button-info"
        disabled
      />
      <div>
        <Button
          label="Submit all"
          class="p-mr-2 p-button-success"
          @click="do_submit_all"
          :disabled="enable_submit_all === false"
        />
        <Button
          label="Edit Again all"
          class="p-mr-2 p-button-success p-button-outlined"
          @click="do_edit_again_all"
          :disabled="enable_edit_again_all === false"
        />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import WeekPicker from "@/components/WeekPicker.vue";
// import MonthPicker from "@/components/MonthPicker.vue";
// import IntervalPicker from "@/components/IntervalPicker.vue";
import Day from "@/components/Day.vue";
import {
  format,
  sub,
  add,
  parse,
  isEqual,
  isAfter,
  parseISO,
  startOfWeek,
  startOfMonth,
} from "date-fns";
import { mapActions, mapState } from "vuex";
import Vue from "vue";
import isSameMonth from "date-fns/isSameMonth";
import isWeekend from "date-fns/isWeekend";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Home",
  data: () => {
    return {
      show_days: [], // days we want to show
      days: [], // days we already have loaded
      att_sums: {},
      att_sum_for_days: 0,
      value: "",
      start_date: null,
      end_date: null,
      range_display: "",
      percent_loaded: 0,
      percent_loaded_by_day: {},
      calendar_value_week: "",
      calendar_value_month: "",
      calendar_value_range: "",
      daily_record_to: {},
      enable_submit_all: false,
      enable_edit_again_all: false,
      daily_record_status: {},
      submit_all: false,
      edit_again_all: false,
    };
  },
  components: {
    Day,
  },
  computed: {
    ...mapState("rest", [
      "api_error",
      "daily_records",
      "found_daily_record_id",
    ]),
    ...mapState(["user_id", "version"]),
    all_submitted: function () {
      // TODO: submit-all does not work reliably
      for (let idx in this.days) {
        for (let k in this.daily_records) {
          let dr_date = parseISO(
            this.daily_records[k].attributes.date.split(".")[0]
          );
          if (isEqual(this.days[idx], dr_date) && !isWeekend(this.days[idx])) {
            // found
            if (this.daily_records[k].attributes.status.name !== "submitted") {
              return false;
            }
          }
        }
      }
      return true;
    },
  },
  created: function () {
    // load and display current week
    this.$store.commit("setUserId", this.$route.params.user_id);
    this.fetch_time_activities().then(() => {
      this.fetch_work_locations().then(() => {
        if (
          this.$route.params.range === "week" &&
          this.$route.params.interval === undefined
        ) {
          this.$router.push(
            "/" +
              this.$route.params.user_id +
              "/" +
              this.$route.params.range +
              "/" +
              this.$route.params.year +
              "/" +
              format(new Date(), "I")
          );
        } else if (
          this.$route.params.range === "month" &&
          this.$route.params.interval === undefined
        ) {
          this.$router.push(
            "/" +
              this.$route.params.user_id +
              "/" +
              this.$route.params.range +
              "/" +
              this.$route.params.year +
              "/" +
              format(new Date(), "M")
          );
        } else {
          console.log("fetch data for", this.$route.params);
          this.update_range();
        }
      });
    });
  },
  methods: {
    ...mapActions("rest", [
      "fetch_time_activities",
      "fetch_work_locations",
      "find_daily_record",
      "fetch_daily_record",
      "fetch_attendance_record",
      "fetch_time_record",
    ]),
    att_sum_changed: function (data) {
      this.att_sums[data.day] = data.sum;
      let sum = 0;
      for (let key in this.att_sums) {
        sum += this.att_sums[key].on;
        sum += this.att_sums[key].off;
        sum += this.att_sums[key].travel;
      }
      this.att_sum_for_days = sum;
    },
    register_daily_record_status: function (data) {
      this.daily_record_status[data.key] = data.data;
      let enable_submit_all = false;
      let enable_edit_again_all = false;
      for (let key in this.daily_record_status) {
        let status = this.daily_record_status[key];
        if (status.submittable === true) {
          enable_submit_all = true;
        }
        if (status.submitted === true) {
          enable_edit_again_all = true;
        }
      }
      this.enable_submit_all = enable_submit_all;
      this.enable_edit_again_all = enable_edit_again_all;
      if (enable_submit_all === false) {
        this.submit_all = false;
      }
      if (enable_edit_again_all === false) {
        this.edit_again_all = false;
      }
    },
    do_submit_all: function () {
      console.log("do_submit_all");
      this.submit_all = true;
    },
    do_edit_again_all: function () {
      console.log("do_edit_again_all");
      this.edit_again_all = true;
    },
    copy_day_to_week: function (data) {
      let src_daily_record = data.daily_record;
      let src_date = parseISO(src_daily_record.attributes.date.split(".")[0]);
      let start_date = startOfWeek(src_date, { weekStartsOn: 1 });
      for (let dow = 0; dow < 7; dow++) {
        Vue.set(this.daily_record_to, start_date, {
          daily_record: src_daily_record,
          opts: data.opts,
        });
        start_date = add(start_date, { days: 1 });
      }
    },
    copy_day_to_month: function (data) {
      let src_daily_record = data.daily_record;
      let src_date = parseISO(src_daily_record.attributes.date.split(".")[0]);
      let start_date = startOfMonth(src_date);
      while (isSameMonth(src_date, start_date)) {
        Vue.set(this.daily_record_to, start_date, {
          daily_record: src_daily_record,
          opts: data.opts,
        });
        start_date = add(start_date, { days: 1 });
      }
    },
    copy_from_last_week: function (data) {
      let this_monday = this.days[0];
      let start_date = sub(this_monday, { days: 7 });
      // fetch all last weeks daily_records
      for (let dow = 0; dow < 7; dow++) {
        this.find_daily_record({
          params: {
            date: format(start_date, "yyyy-MM-dd"),
            user_id: this.user_id,
          },
        }).then(() => {
          if (this.found_daily_record_id) {
            console.log(
              "copy_from_last_week: found dr-id:",
              this.found_daily_record_id
            );
            let daily_record_id = this.found_daily_record_id;
            this.fetch_daily_record({
              params: { id: daily_record_id },
            }).then(() => {
              let daily_record = this.daily_records[daily_record_id];
              let promises = [];
              daily_record.attributes.attendance_record.forEach((att) => {
                promises.push(
                  this.fetch_attendance_record({
                    params: { id: att.id },
                  })
                );
              });
              daily_record.attributes.time_record.forEach((tr) => {
                promises.push(
                  this.fetch_time_record({
                    params: { id: tr.id },
                  })
                );
              });
              Promise.all(promises).then(() => {
                let target_date = parseISO(
                  daily_record.attributes.date.split(".")[0]
                );
                target_date = add(target_date, { days: 7 });
                Vue.set(this.daily_record_to, target_date, {
                  daily_record: daily_record,
                  opts: data.opts,
                });
              });
            });
          }
        });
        start_date = add(start_date, { days: 1 });
      }
    },
    day_percent_loaded: function (data) {
      if (data.percent > 0) {
        if (this.show_days.length > 0) {
          this.days.push(this.show_days.shift());
        }
      }
      this.percent_loaded_by_day[data.day] = data.percent;
      this.percent_loaded = 0;
      this.days.forEach((d) => {
        this.percent_loaded += this.percent_loaded_by_day[d];
      });
      this.percent_loaded = this.percent_loaded / this.days.length;
      console.log("home:", this.percent_loaded);
    },
    increment_interval: function () {
      if (this.$route.params.range === "week") {
        this.calendar_value_week = add(this.calendar_value_week, { weeks: 1 });
        this.calendar_week_changed();
      } else if (this.$route.params.range === "month") {
        this.calendar_value_month = add(this.calendar_value_month, {
          months: 1,
        });
        this.calendar_month_changed();
      }
    },
    decrement_interval: function () {
      if (this.$route.params.range === "week") {
        this.calendar_value_week = sub(this.calendar_value_week, { weeks: 1 });
        this.calendar_week_changed();
      } else if (this.$route.params.range === "month") {
        this.calendar_value_month = sub(this.calendar_value_month, {
          months: 1,
        });
        this.calendar_month_changed();
      }
    },
    update_range: function () {
      if (this.$route.params.range === "week") {
        this.start_date = parse(
          this.$route.params.year + " " + this.$route.params.interval,
          "RRRR I",
          new Date()
        );
        this.end_date = add(this.start_date, { days: 6 });
        this.range_display =
          format(this.start_date, "RRRR") +
          " Wk " +
          format(this.start_date, "I");
        this.calendar_value_week = new Date(this.start_date.getTime());
      } else if (this.$route.params.range === "month") {
        this.start_date = parse(
          this.$route.params.year + " " + this.$route.params.interval,
          "yyyy M",
          new Date(1900, 0, 1, 0, 0, 0)
        );
        this.end_date = sub(add(this.start_date, { months: 1 }), { days: 1 });
        this.range_display =
          this.$route.params.year + " " + format(this.start_date, "MMM");
        this.calendar_value_month = new Date(this.start_date.getTime());
      } else if (this.$route.params.range === "range") {
        this.start_date = parse(
          this.$route.params.year,
          "yyyy-MM-dd",
          new Date(1900, 0, 1, 0, 0, 0)
        );
        this.end_date = parse(
          this.$route.params.interval,
          "yyyy-MM-dd",
          new Date(1900, 0, 1, 0, 0, 0)
        );
        this.range_display =
          format(this.start_date, "yyyy-MM-dd") +
          " to " +
          format(this.end_date, "yyyy-MM-dd");
        this.calendar_value_range = [
          new Date(this.start_date.getTime()),
          new Date(this.end_date.getTime()),
        ];
      }
      console.log("fetch for:", this.start_date, this.end_date);
      this.show_days = [];
      this.days = [];
      let d = this.start_date;
      while (!isAfter(d, this.end_date)) {
        this.show_days.push(d);
        d = add(d, { days: 1 });
      }
      this.days.push(this.show_days.shift());
      let percent_loaded_by_day = {};
      this.show_days.forEach((d) => {
        percent_loaded_by_day[d] = 0;
      });
      this.percent_loaded_by_day = percent_loaded_by_day;
      this.percent_loaded = 0;
    },
    calendar_week_changed: function (data) {
      console.log(data, this.calendar_value_week);
      this.$router.push(
        "/" +
          this.$route.params.user_id +
          "/week/" +
          format(this.calendar_value_week, "RRRR") +
          "/" +
          format(this.calendar_value_week, "I")
      );
    },
    calendar_month_changed: function (data) {
      console.log(data, this.calendar_value_month);
      this.$router.push(
        "/" +
          this.$route.params.user_id +
          "/month/" +
          format(this.calendar_value_month, "yyyy") +
          "/" +
          format(this.calendar_value_month, "M")
      );
    },
    calendar_range_changed: function (data) {
      console.log(data, this.calendar_value_range);
      let start_date = this.calendar_value_range[0];
      let end_date = this.calendar_value_range[1];
      if (end_date !== null) {
        this.$refs["range_picker"].overlayVisible = false;
        this.$router.push(
          "/" +
            this.$route.params.user_id +
            "/range/" +
            format(start_date, "yyyy-MM-d") +
            "/" +
            format(end_date, "yyyy-MM-d")
        );
      }
    },
    copy_atts_from_above: function (date) {
      let from_date = sub(date, { days: 1 });
      for (let idx in this.days) {
        let day = this.days[idx];
        console.log(idx, from_date, day.date);
        if (isEqual(day.date, from_date)) {
          let new_atts = [];
          for (let idx in day.atts) {
            let from_att = day.atts[idx];
            new_atts.push({
              start_time: from_att.start_time,
              end_time: from_att.end_time,
              duration: from_att.duration,
              mobile: from_att.duration,
            });
          }
          console.log(idx);
          this.days[Number(idx) + 1].atts = new_atts;
          break;
        }
      }

      console.log("copy_atts_from_above", date, this.days);
    },
  },
  watch: {
    $route: function () {
      console.log("route changed ... fetch data for", this.$route.params);
      this.update_range();
    },
  },
};
</script>

<style>
.p-calendar > .p-inputtext {
  display: none;
}
.p-field {
  margin-bottom: 0px !important;
}
.p-highlight {
  background-color: var(--surface-b);
}
.p-progressbar-determinate .p-progressbar-value-animate {
  transition: width 10ms ease-in-out !important;
}
</style>
