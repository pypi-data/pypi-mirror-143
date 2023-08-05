"""This module is for the translation mapping data of the
following document:

Document file: index.md
Language: jp
"""

from typing import Dict

MAPPING: Dict[str, str] = {

    '# apysc documentation':
    '',

    'Welcome to apysc documentation! apysc is the Python front-end library (currently developing and only works partially).':  # noqa
    '',

    '## Project links':
    '',

    '- [GitHub](https://github.com/simon-ritchie/apysc)\n  - Stargazers are very welcome!\n- [Twitter](https://twitter.com/apysc)\n  - The progress and updates are informed on Twitter. Please follow!\n- [PyPI](https://pypi.org/project/apysc/)':  # noqa
    '',

    '## Contents':
    '',

    '**Quick start guide**\n\n- [What apysc can do in its current implementation](what_apysc_can_do.md)\n- [Quick start guide](quick_start.md)\n- [Import conventions](import_conventions.md)\n\n---\n\n**Container classes**\n\nThe `Stage` is the apysc overall drawing area container, and the `Sprite` is the container class.\n\n- [Stage class](stage.md)\n- [Sprite class](sprite.md)\n\n---\n\n**Exporting**\n\nThe HTML and JavaScript exporting interfaces.\n\n- [Save overall html interface](save_overall_html.md)\n- [Display on the jupyter interface](display_on_jupyter.md)\n- [Display on the Google Colaboratory interface](display_on_colaboratory.md)\n- [Append js expression interface](append_js_expression.md)\n\n---\n\n**Child-related interfaces**\n\nThe parent class, such as the `Sprite` or `Stage` have the following interfaces:\n\n- [Add child and remove child interfaces](add_child_and_remove_child.md)\n- [Contains interface](contains.md)\n- [Num children interface](num_children.md)\n- [Get child at interface](get_child_at.md)\n\n---\n\n**apysc basic data classes**\n\n- [Why the apysc library does not use the Python built-in data type](why_apysc_doesnt_use_python_builtin_data_type.md)\n- [Funcdamental data classes common value interface](fundamental_data_classes_value_interface.md)\n- [Int and Number classes](int_and_number.md)\n- [Int and Number classes common arithmetic operations](int_and_number_arithmetic_operations.md)\n- [Int and Number classes common comparison operations](int_and_number_comparison_operations.md)\n- [String class](string.md)\n- [String class comparison operations](string_comparison_operations.md)\n- [String class addition and multiplication operations](string_addition_and_multiplication.md)\n- [Boolean class](boolean.md)\n- [Array class](array.md)\n- [Array class append and push interfaces](array_append_and_push.md)\n- [Array class extend and concat interfaces](array_extend_and_concat.md)\n- [Array class insert and insert at interfaces](array_insert_and_insert_at.md)\n- [Array class pop interface](array_pop.md)\n- [Array class remove and remove at interfaces](array_remove_and_remove_at.md)\n- [Array class sort interface](array_sort.md)\n- [Array class reverse interface](array_reverse.md)\n- [Array class slice interface](array_slice.md)\n- [Array class length interface](array_length.md)\n- [Array class join interface](array_join.md)\n- [Array class index of interface](array_index_of.md)\n- [Array class comparison interfaces](array_comparison.md)\n- [Dictionary class](dictionary.md)\n- [Dictionary class generic type settings](dictionary_generic.md)\n- [Dictionary class get interface](dictionary_get.md)\n- [Dictionary class length interface](dictionary_length.md)\n- [Point2D class](point2d.md)\n\n---\n\n**DisplayObject and GraphicsBase classes**\n\nThe `DisplayObject` class is the base class for each display object. The `GraphicsBase` class is the `DisplayObject` subclass and the base class of each graphics class, such as the `Rectangle` class.\n\n- [DisplayObject class](display_object.md)\n- [DisplayObject and GraphicsBase classes basic properties abstract](display_object_and_graphics_base_prop_abstract.md)\n- [DisplayObject class x and y interfaces](display_object_x_and_y.md)\n- [DisplayObject class parent interfaces](display_object_parent.md)\n- [DisplayObject class visible interface](display_object_visible.md)\n- [DisplayObject class get and set css interfaces](display_object_get_and_set_css.md)\n- [DisplayObject class mouse event binding interfaces](display_object_mouse_event.md)\n- [GraphicsBase class rotation around center interface](graphics_base_rotation_around_center.md)\n- [GraphicsBase class rotation around point interfaces](graphics_base_rotation_around_point.md)\n- [GraphicsBase class scale from center interfaces](graphics_base_scale_from_center.md)\n- [GraphicsBase class scale from point interfaces](graphics_base_scale_from_point.md)\n- [GraphicsBase class flip x and flip y interfaces](graphics_base_flip_interfaces.md)\n- [GraphicsBase class skew x and skew y interfaces](graphics_base_skew.md)\n\n---\n\n**Graphics class**\n\nThe `Graphics` class handles each vector graphics drawing.\n\n- [Draw interfaces abstract](draw_interfaces_abstract.md)\n- [Graphics class](graphics.md)\n- [Graphics class begin fill interface](graphics_begin_fill.md)\n- [Graphics class line style interface](graphics_line_style.md)\n- [Graphics class draw rect interface](graphics_draw_rect.md)\n- [Graphics class draw round rect interface](graphics_draw_round_rect.md)\n- [Graphics class draw circle interface](graphics_draw_circle.md)\n- [Graphics class draw ellipse interface](graphics_draw_ellipse.md)\n- [Graphics class move to and line to interfaces](graphics_move_to_and_line_to.md)\n- [Graphics class draw line interface](graphics_draw_line.md)\n- [Graphics class draw dotted line interface](graphics_draw_dotted_line.md)\n- [Graphics class draw dashed line interface](graphics_draw_dashed_line.md)\n- [Graphics class draw round dotted line interface](graphics_draw_round_dotted_line.md)\n- [Graphics class draw dash dotted line interface](graphics_draw_dash_dotted_line.md)\n- [Graphics class draw polygon interface](graphics_draw_polygon.md)\n- [Graphics class fill color interface](graphics_fill_color.md)\n- [Graphics class fill alpha interface](graphics_fill_alpha.md)\n- [Graphics class line color interface](graphics_line_color.md)\n- [Graphics class line alpha interface](graphics_line_alpha.md)\n- [Graphics class line thickness interface](graphics_line_thickness.md)\n- [Graphics class line dot setting interface](graphics_line_dot_setting.md)\n- [Graphics class line dash setting interface](graphics_line_dash_setting.md)\n- [Graphics class line round dot setting interface](graphics_line_round_dot_setting.md)\n- [Graphics class line dash dot setting interface](graphics_line_dash_dot_setting.md)\n\n---\n\n**Common event interfaces**\n\n- [About the handler options type](about_handler_options_type.md)\n- [Event class prevent default and stop propagation interfaces](event_prevent_default_and_stop_propagation.md)\n- [Bind and trigger custom event interfaces](bind_and_trigger_custom_event.md)\n\n---\n\n**MouseEvent class and mouse event binding**\n\n- [MouseEvent interfaces abstract](mouse_event_abstract.md)\n- [Basic mouse event interfaces](mouse_event_basic.md)\n- [Click interface](click.md)\n- [Double click interface](dblclick.md)\n- [Mousedown and mouseup interfaces](mousedown_and_mouseup.md)\n- [Mouseover and mouseout interfaces](mouseover_and_mouseout.md)\n- [Mousemove interface](mousemove.md)\n\n---\n\n**Branch instruction**\n\n- [If class](if.md)\n- [Elif class](elif.md)\n- [Else class](else.md)\n- [Each branch instruction class scope variables reverting setting](branch_instruction_variables_reverting_setting.md)\n- [Return class](return.md)\n\n---\n\n**Loop**\n\n- [For loop class](for.md)\n- [Continue class](continue.md)\n\n---\n\n**Timer**\n\n- [Timer class](timer.md)\n- [TimerEvent class](timer_event.md)\n- [Timer class delay setting](timer_delay.md)\n- [FPS enum](fps.md)\n- [Timer class repeat count setting](timer_repeat_count.md)\n- [Timer class start and stop interfaces](timer_start_and_stop.md)\n- [Timer class timer complete interface](timer_complete.md)\n- [Timer class reset interface](timer_reset.md)\n\n---\n\n**Animation**\n\n- [Animation interfaces abstract](animation_interfaces_abstract.md)\n- [AnimationEvent class](animation_event.md)\n- [Animation duration setting](animation_duration.md)\n- [Animation delay setting](animation_delay.md)\n- [Each animation interface return value](animation_return_value.md)\n- [AnimationBase class start interface](animation_base_start.md)\n- [AnimationBase class animation complete interface](animation_complete.md)\n- [AnimationBase class interfaces method chaining](animation_method_chaining.md)\n- [AnimationBase class target property](animation_base_target.md)\n- [Animation pause and play interfaces](animation_pause_and_play.md)\n- [Animation reset interface](animation_reset.md)\n- [Animation finish interface](animation_finish.md)\n- [Animation reverse interface](animation_reverse.md)\n- [Animation time interface](animation_time.md)\n- [Easing enum](easing_enum.md)\n- [Sequential animation setting](sequential_animation.md)\n- [Animation parallel interface](animation_parallel.md)\n- [Animation move interface](animation_move.md)\n- [Animation x interface](animation_x.md)\n- [Animation y interface](animation_y.md)\n- [Animation width and height interfaces](animation_width_and_height.md)\n- [Animation fill color interface](animation_fill_color.md)\n- [Animation fill alpha interface](animation_fill_alpha.md)\n- [Animation line color interface](animation_line_color.md)\n- [Animation line alpha interface](animation_line_alpha.md)\n- [Animation line thickness interface](animation_line_thickness.md)\n- [Animation radius interface](animation_radius.md)\n- [Animation rotation around center interface](animation_rotation_around_center.md)\n- [Animation rotation around point interface](animation_rotation_around_point.md)\n- [Animation scale x and y from center interfaces](animation_scale_x_and_y_from_center.md)\n- [Animation scale x and y from point interfaces](animation_scale_x_and_y_from_point.md)\n- [Animation skew x interface](animation_skew_x.md)\n\n---\n\n**Debugging**\n\n- [Trace function interface](trace.md)\n- [Set debug mode interface](set_debug_mode.md)\n- [Unset debug mode interface](unset_debug_mode.md)\n\n---\n\n**Testing**\n\n- [JavaScript assertion interface basic behavior](assertion_basic_behavior.md)\n- [Assert equal and assert not equal interfaces](assert_equal_and_not_equal.md)\n- [Assert true and assert false interfaces](assert_true_and_false.md)\n- [Assert arrays equal and arrays not equal interfaces](assert_arrays_equal_and_arrays_not_equal.md)\n- [Assert dicts equal and dicts not equal interfaces](assert_dicts_equal_and_dicts_not_equal.md)\n- [Assert defined and undefined interfaces](assert_defined_and_undefined.md)\n\n---':  # noqa
    '',

}
