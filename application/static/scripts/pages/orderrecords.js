new Vue({
    el: '#app',
    mixins: [mixins.order],
    data: {
        records: [],
        launched: false,
    },
    filters: {
        opnamesource: function (opname) {
            return opname.split('|')[0];
        },
        opnametarget: function (opname) {
            return opname.split('|')[1];
        }
    },
    created: function () {
        let id = Number(new URL(window.location.href).searchParams.get('orderid'));
        if (!id) return;
        this.$get(`/rests/orders/${id}/records`).then(res => {
            this.records = res.data;
            this.launched = true;
        });
    }
});