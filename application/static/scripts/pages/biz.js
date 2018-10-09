new Vue({
    el: '#app',
    mixins: [mixins.biz],
    data: {
        operator: null,
        bizid: null,
        name: '',
        oldname: '',
        remark: '',
        oldremark: '',
        properties: [],
        launched: false
    },
    methods: {
        updatebiz: function () {
            this.$patch(`/rests/bizs/${this.bizid}`, this.getbizmodel()).then(() => {
                this.oldname = this.name;
                this.oldremark = this.remark;
                this.properties.forEach(p => p.oldvalue = p.value);
                this.$toast.show();
            });
        },
        getbizmodel: function () {
            return {
                name: this.name,
                operator: this.operator,
                properties: this.properties.map(p => {
                    return {name: p.name, value: p.value};
                }),
                remark: this.remark
            }
        }
    },
    computed: {
        disableupdate: function () {
            if (this.invalidname(this.name)) return true;
            for (let i = 0; i < this.properties.length; i++) {
                if (this.invalidprop(this.properties[i].value))
                    return true;
            }
            return false;
        }
    },
    created: function () {
        let bizid = Number(new URL(window.location.href).searchParams.get('bizid'));
        if (!bizid) return;
        this.$get(`/rests/bizs/${bizid}`).then(res => {
            const biz = res.data;
            this.bizid = biz.id;
            this.name = biz.name;
            this.remark = biz.remark || '';
            this.properties = biz.properties;
            if (biz.properties && biz.properties.length === 6) {
                this.properties = this.getdefaultproperties();
            }
            this.launched = true;
        });
    }
});