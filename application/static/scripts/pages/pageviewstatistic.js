new Vue({
    el: '#app',
    data: {
        today: 0,
        thisweek: 0,
        thismonth: 0,
        thisseason: 0,
        halfyear: 0,
        thisyear: 0
    },
    created: function () {
        this.$get('/rests/statistics/pageview').then(res => {
            this.today = res.data['today'];
            this.thisweek = res.data['thisweek'];
            this.thismonth = res.data['thismonth'];
            this.thisseason = res.data['thisseason'];
            this.halfyear = res.data['halfyear'];
            this.thisyear = res.data['thisyear'];
            this.loading = false;
        });
    }
});