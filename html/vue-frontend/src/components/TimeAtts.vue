<template>
  <div class="p-d-flex p-jc-end p-ai-center p-mb-1">
    <div class=""></div>
    <div class="p-formgroup-inline" v-if="my_att === null">
      <Skeleton width="479px" :height="float_labels ? '49px' : '33px'" />
    </div>
    <div class="p-formgroup-inline" v-if="my_att !== null">
      <template v-if="debug">
        <div
          class="p-field"
          :style="float_labels ? 'padding-top: 25px' : 'padding-top: 8px'"
        >
          <div>{{ changed }}</div>
        </div>
        <div
          class="p-field"
          :style="float_labels ? 'padding-top: 25px' : 'padding-top: 8px'"
        >
          <div>{{ att_id }} - {{ db_id }}</div>
        </div>
        <div
          class="p-field"
          :style="float_labels ? 'padding-top: 25px' : 'padding-top: 8px'"
        >
          <div>{{ my_att.title }}</div>
        </div>
      </template>

      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'mode' + att_id"
        ></label>
        <span class="p-float-label">
          <Dropdown
            style="width: 10rem"
            :disabled="!enabled"
            :id="'mode' + att_id"
            v-model="my_att.work_location"
            :options="work_locations"
            optionLabel="code"
            optionValue="id"
            scrollHeight="230px"
          >
            <template #value="slotProps">
              <div v-if="slotProps.value">
                <div
                  :class="
                    work_location_by_id(slotProps.value).is_off === 1
                      ? 'my-filled-bg'
                      : ''
                  "
                  v-tooltip.right="
                    work_location_by_id(slotProps.value).description
                  "
                >
                  {{ work_location_by_id(slotProps.value).code }}
                </div>
              </div>
              <span v-else>
                {{ slotProps.placeholder }}
              </span>
            </template>
            <template #option="slotProps">
              <div v-tooltip.right="slotProps.option.description">
                {{ slotProps.option.code }}
              </div>
            </template>
          </Dropdown>
          <label v-if="float_labels" :for="'work_location' + att_id"
            >Work Location</label
          >
        </span>
      </div>

      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'start_time' + att_id"
        ></label>
        <span class="p-float-label">
          <InputText
            :disabled="!enabled"
            :id="'start_time' + att_id"
            size="5"
            @focus.native="$event.target.select()"
            v-model="my_att.start_time"
            @input="start_time_changed"
            @blur="start_time_left"
            :class="{
              'p-invalid': !start_time_is_valid || start_overlaps || too_much,
            }"
            :aria-describedby="'start_time-invalid' + att_id"
          />
          <label v-if="float_labels" :for="'start_time' + att_id">Begin</label>
        </span>
        <small
          v-if="!start_time_is_valid"
          :id="'start_time-invalid' + att_id"
          class="p-error"
          >{{ start_time_invalid_message }}</small
        >
        <small v-else-if="start_overlaps" class="p-error">overlap</small>
        <small v-else-if="too_much" class="p-error">too much</small>
      </div>

      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'end_time' + att_id"
        ></label>
        <span class="p-float-label">
          <InputText
            :disabled="!enabled"
            :id="'end_time' + att_id"
            size="5"
            v-model="my_att.end_time"
            @input="end_time_changed"
            @blur="end_time_left"
            @focus.native="$event.target.select()"
            :class="{
              'p-invalid': !end_time_is_valid || end_overlaps || too_much,
            }"
            :aria-describedby="'end_time-invalid' + att_id"
          />
          <label v-if="float_labels" :for="'end_time' + att_id">End</label>
        </span>
        <small
          v-if="!end_time_is_valid"
          :id="'end_time-invalid' + att_id"
          class="p-error"
          >{{ end_time_invalid_message }}</small
        >
        <small v-else-if="end_overlaps" class="p-error">overlap</small>
        <small v-else-if="too_much" class="p-error">in</small>
      </div>

      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'duration' + att_id"
        ></label>
        <span class="p-float-label">
          <InputText
            :disabled="!enabled"
            :id="'duration' + att_id"
            size="5"
            v-model="my_att.duration"
            @input="duration_changed"
            @blur="duration_left"
            @focus.native="$event.target.select()"
            :class="{ 'p-invalid': !duration_is_valid || too_much }"
            :aria-describedby="'duration-invalid' + att_id"
          />
          <label v-if="float_labels" :for="'duration' + att_id">Duration</label>
        </span>
        <small
          v-if="!duration_is_valid"
          :id="'duration-invalid' + att_id"
          class="p-error"
          >{{ duration_invalid_message }}</small
        >
        <small v-else-if="too_much" class="p-error">total</small>
      </div>

      <div class="p-field" style="width: 2.5rem">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'mode' + att_id"
        ></label>
        <span class="p-float-label">
          <Button
            v-if="!enabled"
            v-show="!(is_last && is_empty)"
            disabled
            :id="'delete' + att_id"
            icon="pi pi-trash"
            class="p-button-rounded p-button-danger p-button-text"
          />
          <Button
            v-else
            v-show="!(is_last && is_empty)"
            :disabled="!enabled"
            :id="'delete' + att_id"
            icon="pi pi-trash"
            v-tooltip.bottom="'remove'"
            class="p-button-rounded p-button-danger p-button-text"
            @click="delete_or_clear(att_id)"
          />
          <label :for="'delete' + att_id"></label>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
//import { minTime } from "date-fns";
import defines from "../defines";
import { mapActions, mapState } from "vuex";
import { validate as uuidValidate } from "uuid";
export default {
  name: "TimeAtts",
  props: {
    daily_record_id: { type: String, required: true },
    att_id: { type: String, required: true },
    start_overlaps: { type: Boolean, required: true },
    end_overlaps: { type: Boolean, required: true },
    too_much: { type: Boolean, required: true },
    day_enabled: { type: Boolean, required: true },
    float_labels: { type: Boolean, required: true },
    is_last: { type: Boolean, required: true },
  },
  data: function () {
    return {
      my_att: null, //this.att,
      db_id: null,
      start_time_is_valid: true,
      start_time_invalid_message: "",
      end_time_is_valid: true,
      end_time_invalid_message: "",
      duration_is_valid: true,
      duration_invalid_message: "",
      created: false,
      loading: false,
    };
  },
  components: {},
  directives: {
    focus: {
      // directive definition
      inserted: function (el) {
        el.focus();
      },
    },
  },
  created: function () {
    if (uuidValidate(this.att_id)) {
      this.my_att = {
        id: this.att_id,
        start_time: "",
        end_time: "",
        duration: "",
        work_location: "2",
        generated: false,
        created: false,
      };
      this.$emit("loaded", { id: this.att_id, att: this.my_att });
    } else {
      this.db_id = this.att_id;
      this.fetch_attendance_record({ params: { id: this.db_id } }).then(
        (resp) => {
          if (resp.status === 200) {
            let att = {
              id: this.att_id,
              duration: "",
              start_time: resp.data.data.attributes.start,
              end_time: resp.data.data.attributes.end,
              work_location: resp.data.data.attributes["work_location"],
              generated: false,
              title: "",
              created: true,
            };
            if (
              resp.data.data.attributes["time_record.wp.durations_allowed"] ===
              1
            ) {
              att.start_time = "--:--";
              att.end_time = "--:--";
              att.duration = String(
                resp.data.data.attributes["time_record.duration"]
              );
              att.generated = true;
              att.title =
                resp.data.data.attributes["time_record.wp.project.name"];
              // delete broken entries
              if (att.duration === "null") {
                this.$emit("delete", this.att_id);
                return;
              }
            }
            if (att.start_time === null) {
              att.start_time = "";
            }
            if (att.end_time === null) {
              att.end_time = "";
            }
            this.my_att = att;
            this.$emit("loaded", { id: this.att_id, att: this.my_att });
            this.validate_form("start_time");
          }
        }
      );
    }
  },
  updated: function () {
    console.log("updated");
    if (
      this.my_att.start_time === "" &&
      this.my_att.end_time === "" &&
      this.my_att.duration === ""
    ) {
      this.start_time_is_valid = true;
      this.start_time_invalid_message = "";
      this.end_time_is_valid = true;
      this.end_time_invalid_message = "";
      this.duration_is_valid = true;
      this.duration_invalid_message = "";
    }
  },
  watch: {
    "my_att.work_location": function () {
      this.validate_form("mobile");
    },
  },
  methods: {
    ...mapActions("rest", [
      "fetch_attendance_record",
      "create_attendance_record",
      "update_attendance_record",
      "delete_attendance_record",
      "delete_linked_time_record",
      "fetch_time_record",
    ]),
    work_location_by_id: function (id) {
      console.log("wlbyid", id);
      for (let idx in this.work_locations) {
        if (this.work_locations[idx].id === id) {
          return this.work_locations[idx];
        }
      }
    },
    delete_or_clear: function (uuid) {
      if (!this.is_last) {
        if (this.db_id !== null) {
          this.delete_attendance_record({
            data: { "@etag": this.stored_data["@etag"] },
            params: { id: this.db_id },
          }).then(() => {
            this.$emit("delete", uuid);
          });
        } else {
          this.$emit("delete", uuid);
        }
      } else {
        this.my_att.start_time = "";
        this.my_att.end_time = "";
        this.my_att.duration = "";
        this.start_time_is_valid = true;
        this.start_time_invalid_message = "";
        this.end_time_is_valid = true;
        this.end_time_invalid_message = "";
        this.duration_is_valid = true;
        this.duration_invalid_message = "";
        this.$emit("clear_error", this.att_id);
      }
    },
    time_string_valid: function (time_string) {
      let hour_rex = /^(\d{1,2}):?$/;
      let hour_minute_rex = /^(\d{1,2}):?(\d{1,2})$/;
      let m;
      var res = { valid: true, matched: "", hour: null, minute: null };

      if ((m = hour_rex.exec(time_string))) {
        let hour = Number.parseInt(m[0]);
        res.matched = "hh";
        res.hour = hour;
        if (hour >= 0 && hour <= 24) {
          // valid input
          return res;
        } else if (hour > 24) {
          res.message = "hh <= 24";
          res.valid = false;
          return res;
        } else {
          res.message = "h, hh, hh:mm";
          res.valid = false;
          return res;
        }
      } else if ((m = hour_minute_rex.exec(time_string))) {
        let hour = Number.parseInt(m[1]);
        let minute = Number.parseInt(m[2]);
        res.matched = "hh:mm";
        res.hour = hour;
        res.minute = minute;
        if (hour >= 0 && hour < 24) {
          if (minute == 0) {
            res.matched = "hh:m";
            return res;
          } else if (minute == 1) {
            res.matched = "hh:m";
            return res;
          } else if (minute == 3) {
            res.matched = "hh:m";
            return res;
          } else if (minute == 4) {
            res.matched = "hh:m";
            return res;
          } else if (minute == 15 || minute == 30 || minute == 45) {
            return res;
          } else {
            res.valid = false;
            res.message = "00, 15, 30, 45";
            return res;
          }
        } else if (hour === 24) {
          if (minute === 0) {
            res.valid = true;
            res.matched = "hh:m";
            return res;
          } else {
            res.valid = false;
            res.message = "only 24:00";
            return res;
          }
        } else if (hour > 24) {
          res.valid = false;
          res.message = "hh <= 24";
          return res;
        }
      } else {
        res.valid = false;
        res.message = "h, hh, hh:mm";
        return res;
      }
      res.valid = false;
      res.message = "";
      return res;
    },
    make_time_string: function (data) {
      console.log("make_timestring", data);
      let res = this.time_string_valid(data);
      if (res.valid === false) {
        console.log(" not valid");
        return data;
      }
      let minute_map = { 0: "00", 1: "15", 3: "30", 4: "45" };
      var time_string = "xx:xx";
      if (res.matched === "hh") {
        time_string = "0" + res.hour + ":00";
        if (time_string.length === 6) {
          time_string = time_string.slice(1);
        }
      } else if (res.matched === "hh:m") {
        time_string = "0" + res.hour + ":" + minute_map[res.minute];
        if (time_string.length === 6) {
          time_string = time_string.slice(1);
        }
      } else if (res.matched === "hh:mm") {
        time_string = "0" + res.hour + ":" + res.minute;
        if (time_string.length === 6) {
          time_string = time_string.slice(1);
        }
      }
      console.log(" return " + time_string);
      console.log(res);
      return time_string;
    },
    duration_string_valid: function (duration_string) {
      let duration_rex = /^(\d+)[.,]?$/;
      let duration_fraction_rex = /^(\d{1,2})[.,](\d{1,2})$/;
      let m;
      var res = { valid: true, matched: "", duration: null };
      var duration = 0;
      var fraction = 0;

      if ((m = duration_rex.exec(duration_string))) {
        duration = Number.parseInt(m[0]);
        res.matched = "d";
        res.duration = parseFloat(duration);
        if (duration > 6 && this.my_att.generated === false) {
          res.message = "only <= 6";
          res.valid = false;
          return res;
        } else if (duration === 0) {
          res.valid = false;
          res.message = "must be > 0";
          return res;
        } else {
          return res;
        }
      } else if ((m = duration_fraction_rex.exec(duration_string))) {
        duration = Number.parseInt(m[1]);
        fraction = Number.parseInt(m[2]);
        res.matched = "d.f";
        res.duration = parseFloat(duration + "." + fraction);
        if (duration >= 0 && duration < 6) {
          if (duration === 0 && fraction === 0) {
            res.valid = false;
            res.message = "must be >0";
            return res;
          } else if (fraction == 0) {
            return res;
          } else if (fraction == 2) {
            res.duration = parseFloat(duration + ".25");
            return res;
          } else if (fraction == 5) {
            res.duration = parseFloat(duration + ".5");
            return res;
          } else if (fraction == 7) {
            res.duration = parseFloat(duration + ".75");
            return res;
          } else if (fraction == 25 || fraction == 50 || fraction == 75) {
            return res;
          } else {
            res.valid = false;
            res.message = ".0, .25, .50, .75";
            return res;
          }
        } else if (duration === 6 && this.my_att.generated === false) {
          if (fraction === 0) {
            res.valid = true;
            return res;
          } else {
            res.valid = false;
            res.message = "only <= 6";
            return res;
          }
        } else if (duration > 6 && this.my_att.generated === false) {
          res.valid = false;
          res.message = "only <= 6";
          return res;
        } else if (duration === 0 && fraction === 0) {
          res.valid = false;
          res.message = "must be >0";
          return res;
        } else if (this.my_att.generated === true) {
          res.valid = true;
          return res;
        }
      } else {
        res.valid = false;
        res.message = "d.dd";
        return res;
      }
      res.valid = false;
      res.message = "error :(";
      return res;
    },
    make_duration_string: function (data) {
      console.log("make_durationstring", data);
      let res = this.duration_string_valid(data);
      if (res.valid === false) {
        return data;
      }
      var duration_string = res.duration.toFixed(2);
      return duration_string;
    },
    clear_error_if_all_is_empty: function () {
      if (
        this.my_att.start_time === "" &&
        this.my_att.end_time === "" &&
        this.my_att.duration === ""
      ) {
        this.$emit("clear_error", this.att_id);
      }
    },
    start_time_changed: function () {
      console.log("start_time_changed", this.my_att.start_time);
      if (this.my_att.start_time.length >= 6) {
        this.my_att.start_time = this.my_att.start_time.slice(0, 5);
      }
      let res = this.time_string_valid(this.my_att.start_time);
      this.start_time_is_valid = res.valid;
      this.start_time_invalid_message = res.message;
      this.$emit("set_error", this.att_id);
      this.clear_error_if_all_is_empty();
    },
    start_time_left: function () {
      console.log("start_time_left");
      this.my_att.start_time = this.make_time_string(this.my_att.start_time);
      if (this.start_time_is_valid === true) {
        this.validate_form("start_time");
      }
    },
    end_time_changed: function () {
      console.log("end_time_changed", this.my_att.end_time);
      if (this.my_att.end_time.length >= 6) {
        this.my_att.end_time = this.my_att.end_time.slice(0, 5);
      }
      let res = this.time_string_valid(this.my_att.end_time);
      this.end_time_is_valid = res.valid;
      this.end_time_invalid_message = res.message;
      this.$emit("set_error", this.att_id);
      this.clear_error_if_all_is_empty();
    },
    end_time_left: function () {
      console.log("end_time_left");
      this.my_att.end_time = this.make_time_string(this.my_att.end_time);
      if (this.end_time_is_valid === true) {
        this.validate_form("end_time");
      }
    },
    duration_changed: function () {
      console.log("duration_changed", this.my_att.duration);
      if (this.my_att.duration.length >= 6) {
        this.my_att.duration = this.my_att.duration.slice(0, 5);
      }
      let res = this.duration_string_valid(this.my_att.duration);
      this.duration_is_valid = res.valid;
      this.duration_invalid_message = res.message;
      this.$emit("set_error", this.att_id);
      this.clear_error_if_all_is_empty();
    },
    duration_left: function () {
      console.log("duration_left");
      this.my_att.duration = this.make_duration_string(this.my_att.duration);
      this.duration_changed();
      if (this.duration_is_valid === true) {
        this.validate_form("duration");
      }
    },
    validate_form: function (who_changed) {
      console.log("validate_form by " + who_changed);

      if (who_changed === "start_time") {
        if (
          this.my_att.end_time &&
          this.time_string_valid(this.my_att.start_time).valid &&
          this.time_string_valid(this.my_att.end_time).valid
        ) {
          if (this.end_time_minutes < this.start_time_minutes) {
            this.start_time_is_valid = false;
            this.start_time_invalid_message = "Begin < End";
          } else {
            this.start_time_is_valid = true;
            this.start_time_invalid_message = "";
            this.end_time_is_valid = true;
            this.end_time_invalid_message = "";
            this.my_att.duration =
              (this.end_time_minutes - this.start_time_minutes) / 60;
            this.duration_changed();
            if (this.duration_is_valid === true) {
              this.my_att.duration = this.make_duration_string(
                this.my_att.duration
              );
            }
          }
        }
      } else if (who_changed === "end_time") {
        if (
          this.my_att.start_time &&
          this.time_string_valid(this.my_att.start_time).valid &&
          this.time_string_valid(this.my_att.end_time).valid
        ) {
          if (this.end_time_minutes < this.start_time_minutes) {
            this.end_time_is_valid = false;
            this.end_time_invalid_message = "End > Begin";
          } else {
            this.start_time_is_valid = true;
            this.start_time_invalid_message = "";
            this.end_time_is_valid = true;
            this.end_time_invalid_message = "";

            this.my_att.duration =
              (this.end_time_minutes - this.start_time_minutes) / 60;
            this.duration_changed();
            if (this.duration_is_valid === true) {
              this.my_att.duration = this.make_duration_string(
                this.my_att.duration
              );
            }
          }
        }
      } else if (who_changed === "duration") {
        if (
          this.my_att.start_time &&
          this.time_string_valid(this.my_att.start_time).valid &&
          this.duration_string_valid(this.my_att.duration).valid
        ) {
          let end_time_minutes =
            this.start_time_minutes + this.duration_minutes;
          let minutes = end_time_minutes % 60;
          let hours = (end_time_minutes - minutes) / 60;
          if (minutes === 0) {
            minutes = "00";
          }
          hours = "0" + hours;
          if (hours.length === 3) {
            hours = hours.slice(1);
          }
          this.my_att.end_time = hours + ":" + minutes;
        } else if (
          !this.my_att.start_time &&
          this.time_string_valid(this.my_att.end_time).valid
        ) {
          let start_time_minutes =
            this.end_time_minutes - this.duration_minutes;
          if (start_time_minutes < 0) {
            this.duration_is_valid = false;
            this.duration_invalid_message = "too big";
            return;
          }
          let minutes = start_time_minutes % 60;
          let hours = (start_time_minutes - minutes) / 60;
          if (minutes === 0) {
            minutes = "00";
          }
          hours = "0" + hours;
          if (hours.length === 3) {
            hours = hours.slice(1);
          }
          this.my_att.start_time = hours + ":" + minutes;
        }
        this.end_time_changed();
        this.start_time_changed();
        if (this.end_time_is_valid === true) {
          this.my_att.end_time = this.make_time_string(this.my_att.end_time);
        }
        if (this.start_time_is_valid === true) {
          this.my_att.start_time = this.make_time_string(
            this.my_att.start_time
          );
        }
      }
      if (this.form_is_valid) {
        if (this.changed) {
          console.log("update or create", this.att_id);
          if (uuidValidate(this.att_id) && this.db_id === null) {
            // create new attendance_record
            let d = {
              start: this.my_att.start_time,
              end: this.my_att.end_time,
              daily_record: this.daily_record_id,
              work_location: this.my_att.work_location,
            };
            this.loading = true;
            this.$emit("set_error", this.att_id); // to block during save
            this.create_attendance_record({ data: d }).then((resp) => {
              console.log(resp);
              this.fetch_attendance_record({
                params: { id: resp.data.data.id },
              }).then((resp) => {
                this.db_id = resp.data.data.id;
                this.loading = false;
                this.$emit("created", this.att_id);
                this.$emit("clear_error", this.att_id);
                this.$emit("update");
              });
            });
          } else {
            // update current record
            let d = {
              start: this.my_att.start_time,
              end: this.my_att.end_time,
              work_location: this.my_att.work_location,
              "@etag": this.stored_data["@etag"],
            };
            this.loading = true;
            this.$emit("set_error", this.att_id); // to block during save
            let time_rec_id = this.stored_data["attributes"]["time_record"];
            let promises = [];
            if (time_rec_id !== null) {
              promises.push(
                this.delete_linked_time_record({
                  data: { "@etag": this.stored_data["@etag"] },
                  params: { id: this.db_id },
                }).then(() => {
                  return this.fetch_time_record({
                    params: { id: time_rec_id },
                  }).then(() => {
                    return this.fetch_attendance_record({
                      params: { id: this.db_id },
                    });
                  });
                })
              );
            }
            Promise.all(promises).then(() => {
              d["@etag"] = this.stored_data["@etag"];
              return this.update_attendance_record({
                data: d,
                params: { id: this.db_id },
              }).then(() => {
                return this.fetch_attendance_record({
                  params: { id: this.db_id },
                }).then(() => {
                  this.loading = false;
                  this.$emit("clear_error", this.att_id);
                  this.$emit("update");
                });
              });
            });
          }
        } else {
          this.$emit("clear_error", this.att_id);
        }
      }
    },
  },
  computed: {
    ...mapState("rest", ["attendance_records", "work_locations"]),
    ...mapState(["debug"]),
    stored_data: function () {
      if (uuidValidate(this.att_id) && this.db_id === null) {
        return {
          attributes: {
            start: "",
            end: "",
            work_location: defines.work_location.mobile,
          },
        };
      } else {
        return this.attendance_records[this.db_id];
      }
    },
    enabled: function () {
      if (this.my_att !== null) {
        return this.day_enabled && !this.my_att.generated && !this.loading;
      } else {
        return false;
      }
    },
    changed: function () {
      if (this.my_att === null) {
        return false;
      }
      return (
        this.my_att.start_time !== "--:--" &&
        this.my_att.end_time !== "--:--" &&
        (this.my_att.start_time !== this.stored_data.attributes.start ||
          this.my_att.end_time !== this.stored_data.attributes.end ||
          this.my_att.work_location !==
            this.stored_data.attributes["work_location"])
      );
    },
    start_time_minutes: function () {
      let parts = this.my_att.start_time.split(":");
      return parseInt(parts[0]) * 60 + parseInt(parts[1]);
    },
    end_time_minutes: function () {
      let parts = this.my_att.end_time.split(":");
      return parseInt(parts[0]) * 60 + parseInt(parts[1]);
    },
    duration_minutes: function () {
      return this.my_att.duration * 60;
    },
    is_empty: function () {
      return (
        this.my_att.start_time === "" &&
        this.my_att.end_time === "" &&
        this.my_att.duration === ""
      );
    },
    form_is_valid: function () {
      return (
        this.my_att.start_time !== "" &&
        this.my_att.end_time !== "" &&
        this.my_att.duration !== "" &&
        this.start_time_is_valid &&
        this.end_time_is_valid &&
        this.duration_is_valid
      );
    },
  },
};
</script>

<style lang="css" scoped>
/* TODO: need to get the dimensions from somewhere - different for each theme!!! */
.my-filled-bg {
  background: var(--surface-border);
  margin: -7px -14px -7px -14px;
  padding: 7px 14px 7px 14px;
}
.my-filled-bg:hover {
  background: var(--surface-border);
}
</style>
