<div class="bs-docs-section">
  <div class="row">
    <div class="col-lg-6 col-lg-offset-3">
      <div class="well bs-component">
        <form class="form-horizontal" action="/view" method="post">
          <legend>Succes!</legend>
          <div class="alert alert-dismissible alert-info">
            Your submission has been approved! The key noted below is your reference code. Store it <strong>carefully</strong>, as you will need it to view and edit your abstract from now on!
          </div>
            <div class="form-group">
              <div class="col-lg-10">
                <input class="form-control" name="reference_code" value="{{var}}" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <div class="col-lg-10">
                  <button type="submit" class="btn btn-primary">View</button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>