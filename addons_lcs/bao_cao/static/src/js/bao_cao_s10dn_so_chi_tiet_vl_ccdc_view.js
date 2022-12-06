odoo.define('bao_cao.bao_cao_s10_so_chi_tiet_vlccdc_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoS10DNController = FormController.extend({
        onFieldChanged: function(field) {
            var domain = [];
            var val = false;
            switch (field) {
                case 'NHOM_VTHH_ID':
                    val = this.getFieldValue('MA_PC_NHOM_VTHH');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_VTHH','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('SAN_PHAM_MANY_IDS').changeDomain(domain);
                    break;
                default:
                    break;
            }
            console.log(val);
        },
       
    });   
    
    var BaoCaoS10DNView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoS10DNController,
        }),
    });
    
    view_registry.add('bao_cao_s10_so_chi_tiet_vlccdc_view', BaoCaoS10DNView);
    return BaoCaoS10DNView;
});
