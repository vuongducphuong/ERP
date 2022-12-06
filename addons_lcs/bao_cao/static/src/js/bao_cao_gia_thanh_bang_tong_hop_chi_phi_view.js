odoo.define('bao_cao.bao_cao_gia_thanh_bang_tong_hop_chi_phi_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoTongHopChiPhiController = FormController.extend({
        onFieldChanged: function(field) {
            var domain = [];
            var val = false;
            switch (field) {
                case 'KY_TINH_GIA_THANH':
                    val = this.getFieldValue('KY_TINH_GIA_THANH');
                    if (val) {
                        domain = [['KY_TINH_GIA_THANH_ID','=', val.id]];
                    }
                    this.getFieldWidget('DOI_TUONG_THCP_MANY_IDS').changeDomain(domain);
                    break;
                default:
                    break;
            }
            console.log(val);
        },
       
    });   
    
    var BaoCaoTongHopChiPhiView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoTongHopChiPhiController,
        }),
    });
    
    view_registry.add('bao_cao_gia_thanh_bang_tong_hop_chi_phi_view', BaoCaoTongHopChiPhiView);
    return BaoCaoTongHopChiPhiView;
});
