Vue.use(swipe);
new Vue({
    el: '#app',
    data: {
        operatorid: undefined,
        operatorname: undefined,
        bizs: [],
        launched: false
    },
    methods: {
        deletebiz: function (biz, index) {
            this.$confirm.show('提示', '确定要删除么?')
                .then(() => this.$delete(`/rests/bizs/${biz['id']}`))
                .then(() => {
                    this.bizs.splice(index, 1);
                    this.$toast.show();
                })
        }
    },
    filters: {
        bizdetailurl: function (biz) {
            return `/public/pages/bizs/${biz['id']}`;
        },
        disableupdatebiz: function (biz) {
            return !biz.newname || (biz.name === biz.newname) || !/^\S{1,10}$/.test(biz.newname);
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
            this.operatorid = operatorid;
            this.operatorname = res.data['operatorname'];
            this.bizs = res.data['bizs'];
            this.launched = true;
        });
    }
});