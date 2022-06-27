<template>
  <div class="p-p-3 p-d-flex p-jc-center p-ai-center">
    <div class="p-mr-2">{{ format_date(day_.date, "PPPP") }}</div>
    <div class="p-mr-2">{{ att_sum_ }}</div>
    <div class="p-mr-2">{{ tr_sum_ }}</div>
    <div class="p-mr-2">
      <Button label="Update from Jira" class="p-mr-2" />
      <Button v-if="day_.status === 'open'" label="Submit" />
      <Button v-if="day_.status === 'submitted'" label="Edit again" />
    </div>
  </div>
</template>

<script>
import { format } from "date-fns";

export default {
  name: "DayTitle",
  props: {
    day: { type: Object, required: true },
    att_sum: { type: Number, required: true },
    tr_sum: { type: Number, required: true },
    status: { type: String, required: true },
  },
  data: function () {
    return {
      format_date: format,
      day_: this.day,
      att_sum_: this.att_sum,
      tr_sum_: this.tr_sum,
    };
  },
  components: {},
  created: function () {
    format(new Date(), "");
  },
  methods: {},
};
</script>
