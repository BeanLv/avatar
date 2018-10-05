new Vue({
    el: '#app',
    data: {
        operatorid: undefined,
        operatorname: undefined,
        bizs: [],
        launched: false
    },
    filters: {
        bizdetailurl: function (biz) {
            return `/pages/biz?bizid=${biz['id']}`;
        },
    },
    computed: {
        createbizurl: function () {
            return '/pages/biz'
        }
    },
    created: function () {
        let operatorid = Number(new URL(window.location.href).searchParams.get('operatorid'));
        if (!operatorid) return;
        this.$get(`/rests/operators/${operatorid}/bizs`).then(res => {
            this.operatorid = operatorid;
            this.operatorname = res.data['operatorname'];
            this.bizs = res.data['bizs'];
            this.launched = true;
        });
    }
});