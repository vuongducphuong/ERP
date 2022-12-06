odoo.define('account_ex.account_ex_chi_phi_chung_can_phan_bo_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var Dialog = require('web.Dialog');

    var ChiPhiChungCanPhanBoController = FormController.extend({
        onViewLoaded: function (e, defer) {
            var self = this;
            var def = defer;

            this.rpc_action({
                model: 'account.ex.chi.phi.do.dang.master',
                method: 'lay_du_lieu_chi_phi_chung',
                // args: {},
                callback: function (result) {
                    if (result) {
                        self.updateUI(result).then(function() {
                            // var nhap_chi_tiet = self.getFieldValue('NHAP_CHI_TIET_LOAI_CPDD_DTTHCP');
                            // var fieldWidget = self.getFieldWidget('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS');
                            // if(nhap_chi_tiet == true){
                            //     fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC'], true);
                            //     fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], false);
                            // }
                        	// else{
                            //     fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC'], false);
                            //     fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], true);
                            // }
                        	if (def) {
								def.resolve();
							}
                        });
                    }
                }
            });
        },
        // onFieldChanged: function(field){
        //     var self = this;
        //     if("NHAP_CHI_TIET_LOAI_CPDD_DTTHCP" == field){
            		
		// 			Dialog.show_message('', 'Nếu tích chọn Nhập chi tiết theo các yếu tố chi phí thì số liệu bạn nhập trên khoản mục Chi phí chung sẽ hiển thị trên yếu tố Chi phí khác. Bạn có muốn tiếp tục thực hiện không?', 'CONFIRM')
		// 			.then(function(result) {
        //                 var fieldWidget = self.getFieldWidget('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS');
		// 				if(result == true){
        //                     if(self.getFieldValue('NHAP_CHI_TIET_LOAI_CPDD_DTTHCP') == true){
        //                         fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC'], true);
        //                         fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], false);
        //                     }
        //                     else{
        //                         fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC'], false);
        //                         fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], true);
        //                     }
        //                 }
		// 		});
        //     }
        // },
    });

    var ChiPhiChungCanPhanBoPView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChiPhiChungCanPhanBoController,
        }),
    });

    view_registry.add('account_ex_chi_phi_chung_can_phan_bo_form_view', ChiPhiChungCanPhanBoPView);

    return ChiPhiChungCanPhanBoPView;
});