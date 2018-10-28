Vue.use(swipe);
Vue.use(hiddenpage);
new Vue({
    el: '#app',
    data: {
        operatorid: undefined,
        operatorname: undefined,
        bizs: [],
        launched: false
    },
    methods: {
        editbiz: function(biz) {
            window.location.href = `/pages/bizedit?bizid=${biz['id']}`;
        },
        deletebiz: function (biz, index) {
            this.$confirm.show('提示', '确定要删除么?')
                .then(() => this.$delete(`/rests/bizs/${biz['id']}`))
                .then(() => {
                    this.bizs.splice(index, 1);
                    this.$toast.show();
                });
        }
    },
    filters: {
        bizdetailurl: function (biz) {
            return `/public/pages/bizs/${biz['id']}`;
        }
    },
    computed: {
        createbizurl: function () {
            return `/pages/bizcreate?operatorid=${this.operatorid}`;
        }
    },
    created: function () {
        let operatorid = Number(new URL(window.location.href).searchParams.get('operatorid'));
        if (!operatorid) return;
        this.$get(`/rests/operators/${operatorid}/bizs`).then(res => {
            res.data['bizs'].forEach(b => b.remark = b.remark || '');
            this.operatorid = operatorid;
            this.operatorname = res.data['operatorname'];
            this.bizs = res.data['bizs'];
            this.launched = true;
        });
    }
});