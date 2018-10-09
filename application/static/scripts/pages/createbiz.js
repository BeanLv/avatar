new Vue({
    el: '#app',
    mixins: [mixins.biz],
    data: {
        operator: null,
        name: '',
        properties: [],
        remark: '',
        launched: false
    },
    methods: {
        createbiz: function () {
            const biz = {
                operator: this.operator,
                name: this.name,
                properties: this.properties,
                remark: this.remark
            };
            this.$post(`/rests/bizs`, biz).then(() => this.$choice.show('成功', '新增成功', '返回', '继续'))
                .then(() => {
                    this.name = '';
                    this.properties = this.getdefaultproperties();
                    this.remark = ''
                })
                .catch(() => {
                    window.history.back();
                });
        }
    },
    computed: {
        disablecreate: function () {
            if (this.isinvalidname(this.name)) return true;
            for (let i = 0; i < this.properties.length; i++) {
                if (this.isinvalidprop(this.properties[i].value)) {
                    return true;
                }
            }
            return false;
        }
    },
    created: function () {
        this.operator = Number(new URL(window.location.href).searchParams.get('operatorid'));
        if (!this.operator) return;
        this.properties = this.getdefaultproperties();
        this.launched = true;
    }
});