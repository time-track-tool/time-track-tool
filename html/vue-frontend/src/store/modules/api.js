import Vapi from "vuex-rest-api";
import axios from "axios";
import Vue from "vue";
import { parseISO } from "date-fns";

let baseUrl =
  process.env.NODE_ENV === "production" ? "" : "http://localhost:8080/t/";

export default new Vapi({
  axios: axios.create({
    headers: { "X-Requested-With": "5T-frontend" },
    withCredentials: true,
  }),
  baseURL: baseUrl,
  state: {
    logged_in: false, // das kommt in keinem property von unten vor
    daily_records: {},
    found_daily_record_id: null,
    created_daily_record_id: null,
    attendance_records: {},
    created_attendance_record: null,
    time_records: {},
    time_activities: [],
    work_locations: [],
    user_dynamic: {},
    update_daily_record_error: {},
    user_dynamic_id_for_date: {},
    api_error: { who: "", error: {} },
    vacation_correction: {},
    dark_mode: false,
    user_etag: "",
    new_tt_iface: false,
    frozen_until: null,
  },
})
  .post({
    action: "login",
    property: "login",
    path: "/",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    onSuccess: (state) => {
      state.logged_in = true;
      state.daily_records = [];
    },
    onError: (state) => {
      state.logged_in = false;
      state.daily_records = [];
    },
  })
  .get({
    action: "logout",
    property: "logout",
    path: "?@action=logout",
    onSuccess: (state) => {
      state.logged_in = false;
      state.daily_records = [];
    },
    onError: (state) => {
      state.logged_in = false;
      state.daily_records = [];
    },
  })
  .get({
    action: "get_new_tt_iface",
    property: "new_tt_iface",
    path: ({ user_id }) => `rest/data/user/${user_id}?@fields=new_tt_iface`,
    onSuccess: (state, payload) => {
      console.log(payload);
      if (payload.data.data.attributes.new_tt_iface === 1) {
        state.new_tt_iface = true;
      } else {
        state.new_tt_iface = false;
      }
      state.user_etag = payload.data.data["@etag"];
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "get_new_tt_iface", error: error };
    },
  })
  .get({
    action: "get_dark_mode",
    property: "get_dark_mode",
    path: ({ user_id }) => `rest/data/user/${user_id}?@fields=dark_mode`,
    onSuccess: (state, payload) => {
      console.log(payload);
      if (payload.data.data.attributes.dark_mode === 1) {
        state.dark_mode = true;
      } else {
        state.dark_mode = false;
      }
      state.user_etag = payload.data.data["@etag"];
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "get_dark_mode", error: error };
    },
  })
  .post({
    action: "set_dark_mode",
    property: "set_dark_mode",
    headers: { "X-HTTP-METHOD-OVERRIDE": "PUT" },
    path: ({ user_id }) => `rest/data/user/${user_id}`,
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "set_dark_mode", error: error };
    },
  })
  .get({
    action: "find_daily_record",
    property: "find_daily_record",
    path: ({ date, user_id }) =>
      `rest/data/daily_record?@verbose=3&@filter=date,user&date=${date}&user=${user_id}`,
    onSuccess: (state, payload) => {
      if (payload.data.data["@total_size"] === 1) {
        state.found_daily_record_id = payload.data.data.collection[0].id;
      } else {
        state.found_daily_record_id = null;
      }
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.found_daily_record = null;
      state.api_error = { who: "find_daily_record", error: error };
    },
  })
  .get({
    action: "fetch_daily_record",
    property: "fetch_daily_record",
    path: ({ id }) => `rest/data/daily_record/${id}?@verbose=3`,
    onSuccess: (state, payload) => {
      Vue.set(state.daily_records, payload.data.data.id, payload.data.data);
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "fetch_daily_record", error: error };
    },
  })
  .post({
    action: "create_daily_record",
    property: "create_daily_record",
    path: "rest/data/daily_record?@verbose=3",
    onSuccess: (state, payload) => {
      state.created_daily_record_id = payload.data.data.id;
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.created_daily_record_id = null;
      state.api_error = { who: "create_daily_record", error: error };
    },
  })
  .post({
    action: "update_daily_record",
    property: "update_daily_record",
    headers: { "X-HTTP-METHOD-OVERRIDE": "PUT" },
    path: ({ id }) => `rest/data/daily_record/${id}`,
    // eslint-disable-next-line no-unused-vars
    onSuccess: (state, payload, axios, { params, data }) => {
      let dr_id = params.id;
      Vue.set(state.update_daily_record_error, dr_id, "");
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      let dr_id = params.id;
      Vue.set(
        state.update_daily_record_error,
        dr_id,
        error.response.data.error.msg
      );
    },
  })
  .post({
    action: "try_daily_record_weekend_allowed",
    property: "try_daily_record_weekend_allowed",
    headers: { "X-HTTP-METHOD-OVERRIDE": "PUT" },
    path: ({ id }) => `rest/data/daily_record/${id}/weekend_allowed`,
    // eslint-disable-next-line no-unused-vars
    onSuccess: (state, payload, axios, { params, data }) => {
      //Vue.set(state.daily_records, payload.data.data.id, Object.assign ({}, state.daily_records[payload.data.data.id],payload.data.data));
      console.log(state.daily_records[payload.data.data.id], payload.data.data);
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      if (
        !(
          error.response.data.error.status === 403 ||
          error.response.data.error.status === 405
        )
      ) {
        state.api_error = {
          who: "try_daily_record_weekend_allowed",
          error: error,
        };
      } else {
        console.log("ERROR from vuex:", error, params, data);
      }
    },
  })
  .get({
    action: "fetch_attendance_record",
    property: "fetch_attendance_record",
    path: ({ id }) =>
      `rest/data/attendance_record/${id}?@verbose=0&@fields=time_record,work_location,work_location.is_off,time_record.wp.durations_allowed,time_record.duration,time_record.wp.project.name,start,end`,
    onSuccess: (state, payload) => {
      Vue.set(
        state.attendance_records,
        payload.data.data.id,
        payload.data.data
      );
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "fetch_attendance_record", error: error };
    },
  })
  .post({
    action: "create_attendance_record",
    property: "create_attendance_record",
    path: "rest/data/attendance_record/",
    onSuccess: (state, payload) => {
      state.created_attendance_record = payload.data;
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.created_attendance_record = null;
      state.api_error = { who: "create_attendance_record", error: error };
    },
  })
  .post({
    action: "update_attendance_record",
    property: "update_attendance_record",
    headers: { "X-HTTP-METHOD-OVERRIDE": "PUT" },
    path: ({ id }) => `rest/data/attendance_record/${id}`,
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "update_attendance_record", error: error };
    },
  })
  .post({
    action: "delete_linked_time_record",
    property: "delete_linked_time_record",
    headers: { "X-HTTP-METHOD-OVERRIDE": "DELETE" },
    path: ({ id }) => `rest/data/attendance_record/${id}/time_record`,
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      if (error.response.status !== 409) {
        state.api_error = { who: "delete_linked_time_record", error: error };
      }
    },
  })
  .post({
    action: "delete_attendance_record",
    property: "delete_attendance_record",
    headers: { "X-HTTP-METHOD-OVERRIDE": "DELETE" },
    path: ({ id }) => `rest/data/attendance_record/${id}`,
    onSuccess: (state, payload) => {
      delete state.attendance_records[payload.data.data.id];
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "delete_attendance_record", error: error };
    },
  })
  .get({
    action: "fetch_time_record",
    property: "fetch_time_record",
    path: ({ id }) =>
      `rest/data/time_record/${id}?@verbose=0&@fields=attendance_record,comment,time_activity.id,wp.id,wp.name,wp.durations_allowed,wp.project.name,wp.project.id,wp.project.is_public_holiday,wp.project.work_location.is_off,duration`,
    onSuccess: (state, payload) => {
      Vue.set(state.time_records, payload.data.data.id, payload.data.data);
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "fetch_time_record", error: error };
    },
  })
  .post({
    action: "create_time_record",
    property: "create_time_record",
    path: "rest/data/time_record/",
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "create_time_record", error: error };
    },
  })
  .post({
    action: "update_time_record",
    property: "update_time_record",
    headers: { "X-HTTP-METHOD-OVERRIDE": "PUT" },
    path: ({ id }) => `rest/data/time_record/${id}`,
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "update_time_record", error: error };
    },
  })
  .post({
    action: "delete_time_record",
    property: "delete_time_record",
    headers: { "X-HTTP-METHOD-OVERRIDE": "DELETE" },
    path: ({ id }) => `rest/data/time_record/${id}`,
    onSuccess: (state, payload) => {
      delete state.time_records[payload.data.data.id];
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "delete_time_record", error: error };
    },
  })
  .get({
    action: "fetch_my_time_wps",
    property: "fetch_my_time_wps",
    path: ({ user_id, date_str }) => {
      return `rest/data/time_wp?@verbose=0&@sort=project.name,name&bookers=${user_id}&time_start=;${date_str}&time_end=-,${date_str};&project.status.active=1&@fields=name,project.name,project.is_public_holiday,project.id,time_start,time_end,project.work_location.is_off,project.no_overtime_day,project.max_hours,durations_allowed,project.is_vacation,project.is_special_leave`;
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.my_time_wps = [];
      state.api_error = { who: "fetch_my_time_wps", error: error };
    },
  })
  .get({
    action: "fetch_public_time_wps",
    property: "fetch_public_time_wps",
    path: ({ date_str }) => {
      return `rest/data/time_wp?@verbose=0&@sort=project.name,name&bookers=-1&is_public=1&time_start=;${date_str}&time_end=-,${date_str};&project.status.active=1&@fields=name,project.name,project.is_public_holiday,project.id,time_start,time_end,project.work_location.is_off,project.no_overtime_day,project.max_hours,durations_allowed,project.is_vacation,project.is_special_leave`;
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.time_wps = [];
      state.api_error = { who: "fetch_public_time_wps", error: error };
    },
  })
  .get({
    action: "fetch_time_activities",
    property: "fetch_time_activities",
    path: "rest/data/time_activity?@sort=name&@verbose=0&@fields=name,id,description,travel&is_valid=1",
    onSuccess: (state, payload) => {
      state.time_activities = payload.data.data.collection;
      state.time_activities.unshift({
        id: "normal_work",
        name: "No selection",
        description: "No selection",
      });
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.time_activities = [];
      state.api_error = { who: "fetch_time_activities", error: error };
    },
  })
  .get({
    action: "fetch_work_locations",
    property: "fetch_work_locations",
    path: "rest/data/work_location?@sort=order&@verbose=0&@fields=code,id,description,is_off,travel&is_valid=1",
    onSuccess: (state, payload) => {
      state.work_locations = payload.data.data.collection;
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.work_locations = [];
      state.api_error = { who: "fetch_work_locations", error: error };
    },
  })
  .get({
    action: "find_user_dynamic",
    property: "find_user_dynamic",
    path: ({ user_id, date_str, end_date_str }) =>
      `rest/data/user_dynamic/?user=${user_id}&valid_from=;${date_str}&valid_to=-,${end_date_str};`,
    // eslint-disable-next-line no-unused-vars
    onSuccess: (state, payload, axios, { params, data }) => {
      if (payload.data.data["@total_size"] === 1) {
        state.user_dynamic_id_for_date[params.date_str] =
          payload.data.data.collection[0].id;
      } else {
        state.user_dynamic_id_for_date[params.date_str] = null;
      }
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.user_dynamic_id_for_date[params.date_str] = null;
      state.api_error = { who: "find_user_dynamic", error: error };
    },
  })
  .get({
    action: "fetch_user_dynamic",
    property: "fetch_user_dynamic",
    path: ({ id }) => `rest/data/user_dynamic/${id}?@verbose=3`,
    // eslint-disable-next-line no-unused-vars
    onSuccess: (state, payload, axios, { params, data }) => {
      Vue.set(
        state.user_dynamic,
        params.date_str,
        payload.data.data.attributes
      );
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "fetch_user_dynamic", error: error };
      Vue.set(state.user_dynamic, params.date_str, null);
    },
  })
  .get({
    action: "search_vacation_correction",
    property: "search_vacation_correction",
    // eslint-disable-next-line no-unused-vars
    path: ({ user_id, date_str, contract_type }) =>
      `rest/data/vacation_correction?user=${user_id}&contract_type=${contract_type}&absolute=1`,
    // eslint-disable-next-line no-unused-vars
    onSuccess: (state, payload, axios, { params, data }) => {
      Vue.set(
        state.vacation_correction,
        params.date_str,
        payload.data.data["@total_size"] !== 0
      );
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "search_vacation_correction", error: error };
      Vue.set(state.vacation_correction, params.date_str, null);
    },
  })
  .get({
    action: "fetch_frozen_until",
    property: "frozen_until",
    path: ({ user_id }) =>
      `rest/data/daily_record_freeze?user=${user_id}&frozen=1&@page_size=1&@fields=date&@sort=-date`,
    // eslint-disable-next-line no-unused-vars
    onSuccess: (state, payload, axios, { params, data }) => {
      state.frozen_until = parseISO(
        payload.data.data.collection[0].date.split(".")[0]
      );
    },
    // eslint-disable-next-line no-unused-vars
    onError: (state, error, axios, { params, data }) => {
      state.api_error = { who: "fetch_frozen_until", error: error };
      state.frozen_until = null;
    },
  })
  .getStore({
    createStateFn: false,
    namespaced: true,
  });
