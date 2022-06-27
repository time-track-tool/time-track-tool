<template>
  <div class="p-d-flex p-ai-center p-mb-1 p-ml-3">
    <div class="p-formgroup-inline" v-if="my_tr === null">
      <Skeleton width="718px" :height="float_labels ? '49px' : '33px'" />
    </div>
    <div class="p-formgroup-inline" v-else>
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
          <div>{{ tr_id }} - {{ db_id }}</div>
        </div>
      </template>
      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'duration' + tr_id"
        ></label>
        <span class="p-float-label">
          <InputText
            :disabled="!enabled || generated || loading"
            :id="'duration' + tr_id"
            size="5"
            v-model="my_tr.duration"
            @input="duration_changed"
            @blur="duration_left"
            @focus.native="$event.target.select()"
            :class="{ 'p-error': !duration_is_valid }"
            :aria-describedby="'duration-invalid' + tr_id"
          />
          <label v-if="float_labels" :for="'duration' + tr_id">Duration</label>
        </span>
        <small
          v-if="!duration_is_valid"
          :id="'duration-invalid' + tr_id"
          class="p-error"
          >{{ duration_invalid_message }}</small
        >
        <small v-else-if="too_much" class="p-error">total</small>
      </div>
      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'duration' + tr_id"
        ></label>
        <span class="p-float-label">
          <template v-if="my_tr.wp.is_off && my_tr.wp.durations_allowed === 1">
            <AutoComplete
              style="width: 23rem"
              :class="my_tr.wp.is_off ? 'p-input-filled' : ''"
              :disabled="!enabled || generated || loading"
              :id="'tc_wp' + tr_id"
              :dropdown="true"
              v-model="my_tr.wp"
              :suggestions="filtered_wps"
              @complete="searchWP($event)"
              field="name"
              @item-select="wp_changed"
              @clear="wp_cleared"
              v-tooltip.right="
                'For this Workpackage you can, but you don’t have to insert a time period on the left side where the Work Location is set to Off'
              "
            >
              <template #item="slotProps">
                <template
                  v-if="
                    slotProps.item.is_off &&
                    slotProps.item.durations_allowed === 1
                  "
                >
                  <div
                    class="my-filled-bg"
                    v-tooltip.right="
                      'For this Workpackage you can, but you don’t have to insert a time period on the left side where the Work Location is set to Off'
                    "
                  >
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
                <template
                  v-else-if="
                    slotProps.item.is_off &&
                    slotProps.item.durations_allowed === 0
                  "
                >
                  <div
                    class="p-button p-button-info my-filled-remove-button-style"
                    v-tooltip.right="
                      'For this Workpackage you have to insert a time period on the left side where the Work Location is set to Off'
                    "
                  >
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
                <template v-else>
                  <div>
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
              </template>
            </AutoComplete>
          </template>
          <template
            v-else-if="my_tr.wp.is_off && my_tr.wp.durations_allowed === 0"
          >
            <AutoComplete
              style="width: 23rem"
              :class="my_tr.wp.is_off ? 'p-input-filled' : ''"
              :disabled="!enabled || generated || loading"
              :id="'tc_wp' + tr_id"
              :dropdown="true"
              v-model="my_tr.wp"
              :suggestions="filtered_wps"
              @complete="searchWP($event)"
              field="name"
              @item-select="wp_changed"
              @clear="wp_cleared"
              v-tooltip.right="
                'For this Workpackage you have to insert a time period on the left side where the Work Location is set to Off'
              "
              class="p-info"
            >
              <template #item="slotProps">
                <template
                  v-if="
                    slotProps.item.is_off &&
                    slotProps.item.durations_allowed === 1
                  "
                >
                  <div
                    class="my-filled-bg"
                    v-tooltip.right="
                      'For this Workpackage you can, but you don’t have to insert a time period on the left side where the Work Location is set to Off'
                    "
                  >
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
                <template
                  v-else-if="
                    slotProps.item.is_off &&
                    slotProps.item.durations_allowed === 0
                  "
                >
                  <div
                    class="p-button p-button-info my-filled-remove-button-style"
                    v-tooltip.right="
                      'For this Workpackage you have to insert a time period on the left side where the Work Location is set to Off'
                    "
                  >
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
                <template v-else>
                  <div>
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
              </template>
            </AutoComplete>
          </template>
          <template v-else>
            <AutoComplete
              style="width: 23rem"
              :class="my_tr.wp.is_off ? 'p-input-filled' : ''"
              :disabled="!enabled || generated || loading"
              :id="'tc_wp' + tr_id"
              :dropdown="true"
              v-model="my_tr.wp"
              :suggestions="filtered_wps"
              @complete="searchWP($event)"
              field="name"
              @item-select="wp_changed"
              @clear="wp_cleared"
            >
              <template #item="slotProps">
                <template
                  v-if="
                    slotProps.item.is_off &&
                    slotProps.item.durations_allowed === 1
                  "
                >
                  <div
                    class="my-filled-bg"
                    v-tooltip.right="
                      'For this Workpackage you can, but you don’t have to insert a time period on the left side where the Work Location is set to Off'
                    "
                  >
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
                <template
                  v-else-if="
                    slotProps.item.is_off &&
                    slotProps.item.durations_allowed === 0
                  "
                >
                  <div
                    class="p-button p-button-info my-filled-remove-button-style"
                    v-tooltip.right="
                      'For this Workpackage you have to insert a time period on the left side where the Work Location is set to Off'
                    "
                  >
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
                <template v-else>
                  <div>
                    {{ slotProps.item.tc_name }} -
                    <i>{{ slotProps.item.wp_name }}</i>
                  </div>
                </template>
              </template>
            </AutoComplete>
          </template>

          <label v-if="float_labels" :for="'tc_wp' + tr_id">Workpackage</label>
        </span>
        <small v-if="!wp_is_valid" :id="'wp-invalid' + tr_id" class="p-error">{{
          wp_invalid_message
        }}</small>
        <small v-if="error_msg" :id="'error_msg' + tr_id" class="p-error">{{
          error_msg
        }}</small>
      </div>
      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'duration' + tr_id"
        ></label>
        <span class="p-float-label">
          <Dropdown
            :disabled="!enabled || generated || loading || !activity_enabled"
            style="width: 13rem"
            :id="'activity' + tr_id"
            v-model="my_tr.time_activity_id"
            :options="time_activities"
            optionLabel="name"
            optionValue="id"
            @change="save_or_create()"
          >
            <template #value="slotProps">
              <div v-if="slotProps.value">
                <div
                  v-tooltip.right="
                    time_activity_by_id(slotProps.value).description
                  "
                >
                  {{ time_activity_by_id(slotProps.value).name }}
                </div>
              </div>
              <span v-else>
                {{ slotProps.placeholder }}
              </span>
            </template>
            <template #option="slotProps">
              <div v-tooltip.right="slotProps.option.description">
                {{ slotProps.option.name }}
              </div>
            </template>
          </Dropdown>
          <label v-if="float_labels" :for="'activity' + tr_id">Activity</label>
        </span>
      </div>
      <div class="p-field">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'comment' + tr_id"
        ></label>
        <span class="p-float-label">
          <Button
            icon="pi pi-comment"
            :id="'comment' + tr_id"
            :class="my_tr.comment ? 'p-button-warning' : ''"
            @click="comment_dialog_open = !comment_dialog_open"
            v-tooltip.bottom="my_tr.comment"
          />
        </span>
      </div>
      <div class="p-field" sstyle="width: 2.5rem; padding-left:">
        <label
          v-if="float_labels"
          class="p-col-fixed"
          style="width: 1px"
          :for="'delete' + tr_id"
        ></label>
        <span class="p-float-label">
          <Button
            v-if="!enabled || generated || loading"
            v-show="!(is_last && is_empty)"
            :id="'delete' + tr_id"
            disabled
            icon="pi pi-trash"
            class="p-button-rounded p-button-danger p-button-text sp-mr-2 sp-ml-2"
          />
          <Button
            v-else
            v-show="!(is_last && is_empty)"
            :id="'delete' + tr_id"
            :disabled="!enabled || generated || loading"
            icon="pi pi-trash"
            v-tooltip.bottom="'remove'"
            class="p-button-rounded p-button-danger p-button-text sp-mr-2 sp-ml-2"
            @click="delete_or_clear(tr_id)"
          />
        </span>
      </div>
    </div>
    <Dialog
      v-if="my_tr !== null"
      header="Header"
      :visible.sync="comment_dialog_open"
      modal
      :closable="false"
      :closeOnEscape="false"
    >
      <template #header>
        <b>Comment for {{ format_date(date, "ccc, PP") }}</b>
      </template>
      <Textarea
        autofocus
        v-model="my_tr.comment"
        :autoResize="true"
        rows="5"
        cols="60"
        :disabled="!enabled || generated || loading"
      />
      <template #footer>
        <Button
          label="Keep & close"
          icon="pi pi-check"
          autofocus
          :disabled="loading"
          @click="
            comment_dialog_open = false;
            save_comment();
          "
        />
        <Button
          :disabled="my_tr.comment === stored_data.attributes.comment"
          label="Revert & close"
          icon="pi pi-times"
          class="p-button-text"
          @click="
            my_tr.comment = stored_data.attributes.comment;
            comment_dialog_open = false;
          "
        />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { format } from "date-fns";
import { mapActions, mapState } from "vuex";
import { validate as uuidValidate } from "uuid";

export default {
  name: "TimeRecs",
  props: {
    daily_record_id: { type: String, required: true },
    tr_id: { type: String, required: true },
    enabled: { type: Boolean, required: true },
    float_labels: { type: Boolean, required: true },
    wps: { type: Array, required: true },
    date: { type: Date, required: true },
    is_last: { type: Boolean, required: true },
    error_msg: { type: String, required: false },
  },
  data: function () {
    return {
      comment_dialog_open: false,
      format_date: format,
      my_tr: null,
      db_id: null,
      filtered_wps: [],
      too_much: false,
      duration_is_valid: false,
      duration_invalid_message: "",
      wp_is_valid: false,
      wp_invalid_message: "",
      generated: false,
      loading: false,
    };
  },
  components: {},
  updated: function () {
    console.log("tr updated", this.my_tr);
  },

  created: function () {
    if (uuidValidate(this.tr_id)) {
      this.my_tr = {
        id: this.tr_id,
        comment: "",
        time_activity_id: "normal_work",
        wp_id: null,
        duration: "",
        wp: "", //{id: "",name:""}
        created: false,
      };
      this.$emit("loaded", { id: this.tr_id, tr: this.my_tr });
    } else {
      this.db_id = this.tr_id;
      this.fetch_time_record({ params: { id: this.db_id } }).then((resp) => {
        if (resp.status === 200) {
          let tr = {
            id: this.tr_id,
            duration: resp.data.data.attributes.duration,
            comment: resp.data.data.attributes.comment || "",
            time_activity_id:
              resp.data.data.attributes["time_activity.id"] || "normal_work",
            wp_id: resp.data.data.attributes["wp.id"],
            wp: "",
            created: true,
          };
          for (let idx in this.wps) {
            let wp = this.wps[idx];
            if (wp.id === tr.wp_id) {
              tr.wp = wp;
              this.wp_is_valid = true;
              break;
            }
          }
          if (resp.data.data.attributes["wp.project.is_public_holiday"] === 1) {
            this.generated = true;
          }
          this.my_tr = tr;
          if (this.my_tr.duration) {
            this.duration_changed();
            if (this.duration_is_valid) {
              this.my_tr.duration = this.make_duration_string(
                this.my_tr.duration
              );
            }
          }
          this.$emit("loaded", { id: this.tr_id, tr: this.my_tr });
        }
      });
    }
  },
  computed: {
    ...mapState("rest", [
      "time_activities",
      "time_records",
      "attendance_records",
    ]),
    ...mapState(["debug"]),
    is_empty: function () {
      return (
        this.my_tr.comment === "" &&
        this.my_tr.duration === "" &&
        this.duration_invalid_message === "" &&
        this.wp_invalid_message === "" &&
        this.my_tr.time_activity_id === "normal_work" &&
        (this.my_tr.wp_id === null || this.my_tr.wp === "")
      );
    },
    changed: function () {
      console.log("changed", Object.assign({}, this.my_tr));
      if (this.my_tr === null) {
        return false;
      }
      return (
        (this.stored_data.attributes.comment || "") !== this.my_tr.comment ||
        this.stored_data.attributes.duration !==
          Number(this.my_tr.duration || "0") ||
        (this.stored_data.attributes["time_activity.id"] || "normal_work") !==
          this.my_tr.time_activity_id ||
        this.stored_data.attributes["wp.id"] !== this.my_tr.wp_id
      );
    },
    stored_data: function () {
      if (uuidValidate(this.tr_id) && this.db_id === null) {
        return {
          attributes: {
            comment: "",
            duration: 0,
            "time_activity.id": "normal_work",
            "wp.id": null,
          },
        };
      } else {
        return this.time_records[this.db_id];
      }
    },
    activity_enabled: function () {
      if (this.my_tr.wp_id) {
        return this.my_tr.wp.is_off !== true;
      }
      return true;
    },
  },
  methods: {
    ...mapActions("rest", [
      "fetch_time_record",
      "update_time_record",
      "delete_time_record",
      "create_time_record",
      "delete_linked_time_record",
      "fetch_attendance_record",
    ]),
    time_activity_by_id: function (id) {
      for (let idx in this.time_activities) {
        if (this.time_activities[idx].id === id) {
          return this.time_activities[idx];
        }
      }
    },
    searchWP(event) {
      console.log(event);
      this.filtered_wps = this.wps.filter(
        (value) =>
          value.is_public_holiday === 0 &&
          value.name.toLowerCase().indexOf(event.query) >= 0
      );
    },
    duration_string_valid: function (duration_string) {
      let res = this.check_duration_string_valid(duration_string);
      if (res.valid === false) {
        this.$emit("set_error", this.tr_id);
      } else {
        this.$emit("clear_error", this.tr_id);
      }
      return res;
    },
    check_duration_string_valid: function (duration_string) {
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

        if (this.my_tr.wp.max_hours != null) {
          if (res.duration > this.my_tr.wp.max_hours) {
            res.valid = false;
            res.message = "must be <= " + this.my_tr.wp.max_hours;
            return res;
          } else {
            res.valid = true;
            res.message = "";
            return res;
          }
        }

        if (duration === 0) {
          res.valid = false;
          res.message = "must be > 0";
          return res;
        } else if (duration > 24) {
          res.valid = false;
          res.message = "must be < 24";
          return res;
        } else {
          return res;
        }
      } else if ((m = duration_fraction_rex.exec(duration_string))) {
        duration = Number.parseInt(m[1]);
        fraction = Number.parseInt(m[2]);
        res.matched = "d.f";
        res.duration = parseFloat(duration + "." + fraction);

        if (this.my_tr.wp.max_hours != null) {
          if (res.duration > this.my_tr.wp.max_hours) {
            res.valid = false;
            res.message = "must be <= " + this.my_tr.wp.max_hours;
            return res;
          } else {
            res.valid = true;
            res.message = "";
            return res;
          }
        }

        if (duration >= 0) {
          if (duration > 24) {
            res.valid = false;
            res.message = "must be < 24";
            return res;
          } else if (duration === 0 && fraction === 0) {
            res.valid = false;
            res.message = "must be > 0";
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
        } else if (duration === 0 && fraction === 0) {
          res.valid = false;
          res.message = "must be > 0";
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
      let res = this.duration_string_valid(data);
      if (res.valid === false) {
        return data;
      }
      var duration_string = res.duration.toFixed(2);
      return duration_string;
    },
    delete_or_clear: function (uuid) {
      if (!this.is_last) {
        if (this.db_id !== null) {
          this.delete_time_record({
            data: { "@etag": this.stored_data["@etag"] },
            params: { id: this.db_id },
          }).then(() => {
            this.$emit("delete", uuid);
          });
        } else {
          this.$emit("delete", uuid);
        }
      } else {
        this.my_tr.duration = "";
        this.my_tr.comment = "";
        this.my_tr.time_activity_id = "normal_work";
        this.my_tr.wp_id = null;
        this.my_tr.wp = { id: "", name: "" };
        this.duration_is_valid = false;
        this.duration_invalid_message = "";
        this.wp_is_valid = false;
        this.wp_invalid_message = "";
        this.$emit("clear_error", this.tr_id);
      }
    },
    save_or_create: function () {
      if (!this.duration_is_valid || !this.wp_is_valid || !this.changed) {
        console.log("dont save");
        return;
      }
      if (uuidValidate(this.tr_id) && this.db_id === null) {
        // create new time_record
        let d = {
          daily_record: this.daily_record_id,
          duration: this.my_tr.duration,
          wp: this.my_tr.wp_id,
        };
        if (this.my_tr.time_activity_id !== "normal_work") {
          d.time_activity = this.my_tr.time_activity_id;
        }
        if (this.my_tr.comment !== "") {
          d.comment = this.my_tr.comment;
        }
        this.loading = true;
        this.$emit("set_error", this.tr_id); // to block during save
        this.create_time_record({ data: d }).then((resp) => {
          console.log("created:", resp);
          this.db_id = resp.data.data.id;
          this.fetch_time_record({
            params: { id: resp.data.data.id },
          }).then(() => {
            this.loading = false;
            this.$emit("clear_error", this.tr_id);
            this.$emit("created", this.tr_id);
            this.$emit("update");
          });
        });
      } else {
        // update current record
        this.loading = true;
        this.$emit("set_error", this.tr_id); // to block during save
        let d = {
          duration: this.my_tr.duration,
          wp: this.my_tr.wp_id,
          comment: this.my_tr.comment,
          "@etag": this.stored_data["@etag"],
        };
        let atts = this.stored_data["attributes"];
        let promises = [];
        if (atts["attendance_record"] !== undefined) {
          if (atts["attendance_record"][0] !== undefined) {
            console.log(
              "need to delete_linked_time_record of",
              this.stored_data["attributes"]["attendance_record"][0]
            );
            let att_rec_id =
              this.stored_data["attributes"]["attendance_record"][0];
            promises.push(
              this.delete_linked_time_record({
                data: { "@etag": this.attendance_records[att_rec_id]["@etag"] },
                params: { id: att_rec_id },
              })
                .then(() => {
                  return this.fetch_attendance_record({
                    params: { id: att_rec_id },
                  }).then(() => {
                    return this.fetch_time_record({
                      params: { id: this.db_id },
                    });
                  });
                })
                .catch((data) => {
                  console.log("error:", data);
                  if (data.response.status === 409) {
                    console.log("att_record is retired, but that's ok");
                  }
                })
                .finally(() => {
                  return this.fetch_time_record({
                    params: { id: this.db_id },
                  });
                })
            );
          }
        }

        if (this.my_tr.time_activity_id === "normal_work") {
          d.time_activity = -1; //this.my_tr.time_activity_id;
        } else {
          d.time_activity = this.my_tr.time_activity_id;
        }

        Promise.all(promises).then(() => {
          d["@etag"] = this.stored_data["@etag"];
          return this.update_time_record({
            data: d,
            params: { id: this.db_id },
          })
            .then(() => {
              this.fetch_time_record({
                params: { id: this.db_id },
              });
            })
            .then(() => {
              this.loading = false;
              this.$emit("clear_error", this.tr_id);
              this.$emit("update");
            });
        });
      }
    },
    save_comment: function () {
      if (this.duration_is_valid === true && this.wp_is_valid === true) {
        this.save_or_create();
      }
    },
    duration_changed: function () {
      console.log("duration_changed", this.my_tr.duration);
      if (this.my_tr.duration.length >= 6) {
        this.my_tr.duration = this.my_tr.duration.slice(0, 5);
      }
      let res = this.duration_string_valid(this.my_tr.duration);
      this.duration_is_valid = res.valid;
      this.duration_invalid_message = res.message;
      // even if the string is valid, block "submit" button in
      // day, duration_left releases the block
      this.$emit("set_error", this.tr_id);
    },
    duration_left: function () {
      console.log("duration_left");
      this.my_tr.duration = this.make_duration_string(this.my_tr.duration);
      this.duration_changed();
      this.save_or_create();
    },
    wp_cleared: function (event) {
      this.my_tr.wp_id = "";
      this.wp_changed(event);
    },
    wp_changed: function (event) {
      console.log("wp_changed", event, this.my_tr.wp);
      if (typeof this.my_tr.wp !== "object") {
        // XXX: we should also check if it is in wps ?
        this.wp_is_valid = false;
        this.wp_invalid_message = "sorry, you must select one";
      } else {
        if (this.my_tr.wp.id === "") {
          this.wp_is_valid = false;
          this.wp_invalid_message = "sorry, you must select one";
        } else {
          this.wp_is_valid = true;
          this.wp_invalid_message = "";
          this.my_tr.wp_id = this.my_tr.wp.id;
          if (this.my_tr.wp.is_off === true) {
            this.my_tr.time_activity_id = "normal_work";
          }
          this.duration_changed();
          this.save_or_create();
        }
      }
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
  background: var(--surface-hover);
}
.my-filled-remove-button-style {
  margin: -7px -14px -7px -14px;
  padding: 7px 14px 7px 14px;
  border: 0px;
  display: inherit;
  text-align: inherit;
  cursor: inherit;
  user-select: inherit;
  overflow: inherit;
  position: inherit;
  border-radius: inherit;
}
.my-filled-remove-button-style:hover {
  background: var(--surface-hover);
  color: var(--text-color);
}
</style>
