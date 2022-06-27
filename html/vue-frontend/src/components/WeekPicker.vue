<template>
  <div>
    <Button icon="pi pi-angle-left" class="p-mr-2" @click="prev_week" />
    <Dropdown
      v-model="selectedWeek"
      :options="weekOptions"
      optionLabel="title"
      placeholder="Select Week"
      class="p-mr-2"
      @change="changed"
    />
    <Button icon="pi pi-angle-right" class="" @click="next_week" />
  </div>
</template>

<script>
import {
  subWeeks,
  addWeeks,
  startOfISOWeek,
  endOfISOWeek,
  format,
} from "date-fns";

export default {
  name: "WeekPicker",
  props: {
    pastWeeks: { type: Number, default: 20 },
    futureWeeks: { type: Number, default: 2 },
  },
  data: () => {
    return {
      selectedWeek: null,
      weekOptions: [],
    };
  },
  components: {},
  created: function () {
    this.create_week_options();
    this.selectedWeek = this.weekOptions[this.pastWeeks];
  },
  methods: {
    create_week_options: function () {
      let now = new Date();
      let sow = subWeeks(startOfISOWeek(now), this.pastWeeks);
      let eow = endOfISOWeek(sow);
      let res = [];

      for (let cnt = 0; cnt < this.pastWeeks + this.futureWeeks; cnt++) {
        res.push({
          title: "KW" + format(sow, "II (P") + " - " + format(eow, "P)"),
          start: sow,
        });
        sow = addWeeks(sow, 1);
        eow = addWeeks(eow, 1);
      }
      this.weekOptions = res;
    },
    changed: function () {
      this.$emit("update:selectedWeek", this.selectedWeek);
    },
    prev_week: function () {
      let curr = this.weekOptions.indexOf(this.selectedWeek);
      if (curr > 0) {
        this.selectedWeek = this.weekOptions[curr - 1];
      }
      this.changed();
    },
    next_week: function () {
      let curr = this.weekOptions.indexOf(this.selectedWeek);
      console.log(curr);
      if (curr < this.weekOptions.length - 1) {
        this.selectedWeek = this.weekOptions[curr + 1];
      }
      this.changed();
    },
  },
};
</script>
