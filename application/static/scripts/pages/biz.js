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
        editing: false,
        launched: false
    },
    methods: {
        updatebiz: function () {
            this.$patch(`/rests/bizs/${this.bizid}`, this.getbizmodel()).then(() => {
                this.oldname = this.name;
                this.oldremark = this.oldremark;
                this.$toast.show();
            });
        },
        getbizmodel: function () {
            return {
                name: this.name,
                operator: this.operator,
                properties: this.properties,
                remark: this.remark
            }
        }
    },
    filters: {
        invalidname: function (name) {
            return !name || !this.namereg.test(name);
        },
        invalidprop: function (prop) {
            return !prop || !this.propreg.test(prop);
        }
    },
    computed: {
        disablecreate: function () {
            if (!this.name || !this.namereg.test(name)) return true;
            this.properties.forEach(p => {
                if (this.filters.invalidprop(p.value))
                    return true;
            });
            return false;
        },
        disableupdate: function () {
            if (!this.name || !this.namereg.test(name)) return true;
            this.properties.forEach(p => {
                if (this.filters.invalidprop(p.value))
                    return true;
            });
        }
    },
    created: function () {
        let defaultproperties = [
            {name: '属性一', value: '', oldvalue: '', seq: 1},
            {name: '属性二', value: '', oldvalue: '', seq: 2},
            {name: '属性三', value: '', oldvalue: '', seq: 3},
            {name: '属性四', value: '', oldvalue: '', seq: 4},
            {name: '属性五', value: '', oldvalue: '', seq: 5},
            {name: '属性六', value: '', oldvalue: '', seq: 6}
        ];
        let operatorid = Number(new URL(window.location.href).searchParams.get('operatorid'));
        if (!operatorid) return;
        this.operator = operatorid;
        this.namereg = new RegExp('^\\S{1,10}$');
        this.propreg = new RegExp('^\\S{1, 32}$');
        let bizid = Number(new URL(window.location.href).searchParams.get('bizid'));
        if (!bizid) {
            this.properties = defaultproperties;
            this.bizid = null;
            this.launched = true;
        } else {
            this.$get(`/rests/bizs/${bizid}`).then(res => {
                const biz = res.data;
                this.bizid = biz.id;
                this.name = biz.name;
                this.remark = biz.remark || '';
                if (biz.properties && biz.properties.length === 6) {
                    biz.properties.forEach(p => p['oldvalue'] = '');
                    this.properties = biz.properties;
                } else {
                    this.properties = defaultproperties;
                }
                this.launched = true;
            });
        }
    }
});